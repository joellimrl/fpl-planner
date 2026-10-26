"""Validate private state without echoing private payloads in errors."""
from collections import Counter
from copy import deepcopy


def _integer(value, lo, hi):
    return type(value) is int and lo <= value <= hi


def validate_state(state, players, next_gw):
    if not isinstance(state, dict):
        raise ValueError('Invalid squad state')
    if state.get('effective_gameweek') != next_gw:
        raise ValueError('Private squad state is stale; refresh for the next gameweek')
    try:
        assert _integer(state['bank'], 0, 10000)
        assert _integer(state['free_transfers'], 0, 5)
        assert isinstance(state['squad'], list) and len(state['squad']) == 15
        by_id = {p['id']: p for p in players}
        ids = [p['element'] for p in state['squad']]
        assert len(set(ids)) == 15 and all(type(i) is int and i in by_id for i in ids)
        assert Counter(by_id[i]['position'] for i in ids) == {1: 2, 2: 5, 3: 5, 4: 3}
        assert max(Counter(by_id[i]['team'] for i in ids).values()) <= 3
        result = deepcopy(state)
        for pick in result['squad']:
            assert _integer(pick['purchase_price'], 1, 1000)
            assert _integer(pick['selling_price'], 1, 1000)
            current = by_id[pick['element']]['price']
            purchase = pick['purchase_price']
            pick['selling_price'] = current if current <= purchase else purchase + (current - purchase) // 2
        return result
    except (AssertionError, KeyError, TypeError, ValueError):
        raise ValueError('Invalid squad state') from None
