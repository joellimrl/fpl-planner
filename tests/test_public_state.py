import copy
import unittest
from tests.helpers import league


def public_fixture(weeks=3):
    players, state = league()
    boot = {'elements': [dict(id=p['id'], now_cost=52, cost_change_start=2)
                         for p in players],
            'events': [dict(id=i, is_current=i == weeks, is_previous=i == weeks-1,
                            overrides={'rules': {}}) for i in range(1, weeks+1)],
            'game_settings': {'max_extra_free_transfers': 4,
                              'element_sell_at_purchase_price': False,
                              'transfers_sell_on_fee': 0.5}}
    rows = [dict(event=i, bank=250, event_transfers=0, event_transfers_cost=0)
            for i in range(1, weeks+1)]
    picks = [dict(element=p['element']) for p in state['squad']]
    data = {'entry/42/': {'started_event': 1, 'current_event': weeks},
            'entry/42/history/': {'current': rows, 'chips': []},
            'entry/42/transfers/': []}
    for row in rows:
        data[f"entry/42/event/{row['event']}/picks/"] = {
            'active_chip': None, 'picks': copy.deepcopy(picks),
            'entry_history': copy.deepcopy(row)}

    class Client:
        def get(self, path):
            return copy.deepcopy(data[path])
    return boot, data, Client()


def transfer(event, out=4, incoming=9, cost=51, sale=50, time='12:00:00'):
    return dict(event=event, element_out=out, element_in=incoming,
                element_in_cost=cost, element_out_cost=sale,
                time=f'2026-09-{event:02d}T{time}Z')


class PublicStateTests(unittest.TestCase):
    def load(self, boot, client, next_gw=None):
        from fpl_planner.public_state import load_public_state
        return load_public_state(client, boot, 42, next_gw or len(boot['events'])+1)

    def test_initial_prices_and_published_bank_without_credentials(self):
        boot, data, client = public_fixture()
        state = self.load(boot, client)
        self.assertEqual(state['effective_gameweek'], 4)
        self.assertEqual(state['bank'], 250)
        self.assertEqual(state['free_transfers'], 3)
        self.assertEqual(state['squad'][0]['purchase_price'], 50)
        self.assertEqual(state['squad'][0]['selling_price'], 51)
        self.assertEqual(state['baseline']['published_gameweek'], 3)

    def test_transfer_and_rebuy_use_actual_cost_not_original_price(self):
        boot, data, client = public_fixture()
        data['entry/42/transfers/'] = [transfer(3, 9, 4, 54, 51), transfer(2)]
        for gw, bank in [(2, 249), (3, 246)]:
            data['entry/42/history/']['current'][gw-1].update(
                bank=bank, event_transfers=1)
            data[f'entry/42/event/{gw}/picks/']['entry_history'].update(
                bank=bank, event_transfers=1)
        state = self.load(boot, client)
        pick = next(p for p in state['squad'] if p['element'] == 4)
        self.assertEqual(pick['purchase_price'], 54)
        self.assertEqual(pick['selling_price'], 52)
        self.assertEqual(state['bank'], 246)
        self.assertEqual(state['free_transfers'], 1)

    def test_rolls_cap_at_five(self):
        boot, _, client = public_fixture(8)
        self.assertEqual(self.load(boot, client)['free_transfers'], 5)

    def test_hits_are_reconciled_with_available_transfers(self):
        boot, data, client = public_fixture(2)
        data['entry/42/transfers/'] = [transfer(2), transfer(2, 5, 10)]
        row = data['entry/42/history/']['current'][1]
        row.update(bank=248, event_transfers=2, event_transfers_cost=4)
        target = data['entry/42/event/2/picks/']
        target['entry_history'].update(row)
        target['picks'] = [dict(element={4:9, 5:10}.get(p['element'], p['element']))
                           for p in target['picks']]
        self.assertEqual(self.load(boot, client)['free_transfers'], 1)
        row['event_transfers_cost'] = 0
        with self.assertRaises(ValueError): self.load(boot, client)

    def test_wildcard_keeps_allowance_and_permanent_purchases(self):
        boot, data, client = public_fixture()
        data['entry/42/history/']['chips'] = [dict(event=3, name='wildcard')]
        row = data['entry/42/history/']['current'][2]
        row.update(bank=249, event_transfers=1)
        target = data['entry/42/event/3/picks/']
        target['entry_history'].update(row)
        target['active_chip'] = 'wildcard'
        target['picks'] = [dict(element=9 if p['element']==4 else p['element'])
                           for p in target['picks']]
        data['entry/42/transfers/'] = [transfer(3)]
        state = self.load(boot, client)
        self.assertEqual(state['free_transfers'], 2)
        self.assertEqual(state['bank'], 249)
        self.assertIn(9, [p['element'] for p in state['squad']])

    def test_freehit_restores_squad_bank_and_retains_allowance(self):
        boot, data, client = public_fixture()
        data['entry/42/history/']['chips'] = [dict(event=3, name='freehit')]
        data['entry/42/history/']['current'][2].update(bank=249, event_transfers=1)
        target = data['entry/42/event/3/picks/']
        target['entry_history'].update(bank=249, event_transfers=1)
        target['active_chip'] = 'freehit'
        target['picks'][2]['element'] = 9
        data['entry/42/transfers/'] = [transfer(3)]
        state = self.load(boot, client)
        self.assertEqual(state['bank'], 250)
        self.assertEqual(state['free_transfers'], 2)
        self.assertEqual(state['baseline']['squad_gameweek'], 2)
        self.assertNotIn(9, [p['element'] for p in state['squad']])

    def test_unpublished_transactions_ignored(self):
        boot, data, client = public_fixture()
        data['entry/42/transfers/'] = [transfer(4)]
        self.assertEqual(self.load(boot, client)['bank'], 250)

    def test_missing_history_or_purchase_fields_or_squad_mismatch_rejected(self):
        for damage in ('history', 'price', 'squad', 'bank', 'late', 'rollover', 'override'):
            with self.subTest(damage=damage):
                boot, data, client = public_fixture()
                if damage == 'history': data['entry/42/history/']['current'].pop(1)
                if damage == 'price': del boot['elements'][0]['cost_change_start']
                if damage == 'squad': data['entry/42/event/3/picks/']['picks'][2]['element'] = 9
                if damage == 'bank': data['entry/42/history/']['current'][2]['bank'] = 249
                if damage == 'late': data['entry/42/']['started_event'] = 2
                if damage == 'rollover': data['entry/42/']['current_event'] = 4
                if damage == 'override': boot['events'][1]['overrides']['rules'] = {'unknown': 7}
                with self.assertRaises(ValueError): self.load(boot, client)

    def test_old_freehit_transactions_never_leak_into_permanent_cost(self):
        boot, data, client = public_fixture(4)
        data['entry/42/history/']['chips'] = [dict(event=2, name='freehit')]
        data['entry/42/history/']['current'][1].update(bank=249, event_transfers=1)
        data['entry/42/transfers/'] = [transfer(2)]
        state = self.load(boot, client)
        self.assertEqual(state['free_transfers'], 3)
        self.assertNotIn(9, [p['element'] for p in state['squad']])

    def test_unknown_chip_fails(self):
        boot, data, client = public_fixture()
        data['entry/42/history/']['chips'] = [dict(event=2, name='newchip')]
        with self.assertRaises(ValueError): self.load(boot, client)
