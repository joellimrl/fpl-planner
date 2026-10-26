import unittest
from collections import Counter
from tests.helpers import league


class OptimiseTests(unittest.TestCase):
    def test_rollover_and_hits(self):
        from fpl_planner.optimise import transfer_accounting
        self.assertEqual(transfer_accounting(5,0),(0,5))
        self.assertEqual(transfer_accounting(0,2),(8,1))
        self.assertEqual(transfer_accounting(3,2),(0,2))

    def test_legal_hold_budget_and_captain(self):
        from fpl_planner.optimise import solve
        players,state=league()
        plan=solve(players,state,[9,10],{'time_limit':10},hold_now=True)
        first=plan['weeks'][0]
        self.assertEqual(first['buys'],[])
        self.assertEqual(first['bank'],10)
        self.assertEqual(len(first['starters']),11)
        self.assertIn(first['captain'],first['starters'])
        positions=Counter(next(p for p in players if p['id']==i)['position'] for i in first['starters'])
        self.assertEqual(positions[1],1);self.assertGreaterEqual(positions[2],3)
        self.assertGreaterEqual(positions[3],2);self.assertGreaterEqual(positions[4],1)

    def test_gain_exceeds_hit_and_funds_constrain(self):
        from fpl_planner.optimise import compare
        players,state=league();state['free_transfers']=0
        ids={p['element'] for p in state['squad']}
        target=next(p for p in players if p['position']==4 and p['id'] not in ids)
        target['forecasts']={9:20.,10:20.}
        result=compare(players,state,[9,10],{'time_limit':10})
        self.assertIn(target['id'],result['best']['weeks'][0]['buys'])
        self.assertEqual(result['best']['weeks'][0]['hit'],4)
        self.assertGreater(result['gain'],0)
        target['price']=500
        result=compare(players,state,[9],{'time_limit':10})
        self.assertNotIn(target['id'],result['best']['weeks'][0]['squad'])

    def test_initial_discount_survives_hold_not_rebuy(self):
        from fpl_planner.optimise import solve
        players,state=league()
        # Initial player was bought at 50; market fell to 40. Sale must receive 40.
        original=state['squad'][0];p=next(p for p in players if p['id']==original['element'])
        p['price']=40;original['selling_price']=40
        plan=solve(players,state,[9,10],{'time_limit':10},hold_now=True)
        for week in plan['weeks']:
            self.assertGreaterEqual(week['bank'],0)
        self.assertEqual(plan['weeks'][0]['next_free_transfers'],2)


if __name__=='__main__':unittest.main()
