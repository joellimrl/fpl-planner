"""Reconstruct a permanent squad from public, deadline-locked FPL records."""


def _require(condition):
    if not condition:
        raise ValueError('Public baseline is incomplete, inconsistent or uses unsupported rules')


def _money(value):
    _require(type(value) is int and 0 <= value <= 10000)
    return value


def _ids(picks):
    ids = [p['element'] for p in picks]
    _require(len(ids) == 15 and len(set(ids)) == 15)
    return set(ids)


def load_public_state(client, bootstrap, entry_id, next_gw):
    """Return the next-deadline baseline; never incorporate unpublished moves.

    Late entries cannot recover precise initial costs from season-start prices.
    Unknown event overrides are rejected until their rules are implemented.
    HTTP failures propagate so the caller cannot publish a partial update.
    """
    _require(type(entry_id) is int and entry_id > 0)
    prefix = f'entry/{entry_id}/'
    entry = client.get(prefix)
    published = max((e['id'] for e in bootstrap['events']
                     if e.get('is_current') or e.get('is_previous')), default=0)
    _require(published > 0 and entry['current_event'] == published)
    _require(next_gw == published + 1 and entry['started_event'] == 1)
    settings = bootstrap.get('game_settings', {})
    _require(settings.get('max_extra_free_transfers', 4) == 4)
    _require(settings.get('transfers_sell_on_fee', 0.5) == 0.5)
    _require(not settings.get('element_sell_at_purchase_price', False))
    for event in bootstrap['events']:
        _require(not event.get('overrides', {}).get('rules'))

    history = client.get(prefix + 'history/')
    rows = sorted((r for r in history['current'] if r['event'] <= published),
                  key=lambda r: r['event'])
    _require([r['event'] for r in rows] == list(range(1, published+1)))
    chips = {}
    for chip in history['chips']:
        if chip['event'] > published:
            continue
        _require(chip['event'] not in chips)
        _require(chip['name'] in {'wildcard', 'freehit', 'bboost', '3xc'})
        chips[chip['event']] = chip['name']
    _require(chips.get(1) not in {'freehit', 'wildcard'})

    latest = client.get(prefix + f'event/{published}/picks/')
    _require(latest.get('active_chip') == chips.get(published))
    for field in ('event', 'bank', 'event_transfers', 'event_transfers_cost'):
        _require(latest['entry_history'][field] == rows[-1][field])
    squad_gw = published
    if chips.get(published) == 'freehit':
        squad_gw -= 1
        _require(squad_gw > 0 and chips.get(squad_gw) != 'freehit')
    permanent = latest if squad_gw == published else client.get(
        prefix + f'event/{squad_gw}/picks/')
    initial = permanent if squad_gw == 1 else client.get(prefix + 'event/1/picks/')
    initial_ids = _ids(initial['picks'])
    by_id = {p['id']: p for p in bootstrap['elements']}
    _require(all(pid in by_id and 'cost_change_start' in by_id[pid] for pid in initial_ids))
    purchases = {pid: by_id[pid]['now_cost'] - by_id[pid]['cost_change_start']
                 for pid in initial_ids}
    _require(all(type(v) is int and 0 < v <= 1000 for v in purchases.values()))
    bank = _money(rows[0]['bank'])
    _require(sum(purchases.values()) + bank == settings.get('squad_total_spend', 1000))
    transactions = client.get(prefix + 'transfers/')
    transactions = sorted((t for t in transactions if 1 < t['event'] <= published),
                          key=lambda t: (t['event'], t['time']))
    allowance = 1  # Available after the initial, unlimited-transfer deadline.
    for row in rows[1:]:
        gw = row['event']
        moves = [t for t in transactions if t['event'] == gw]
        chip = chips.get(gw)
        count = row['event_transfers']
        _require(type(count) is int and count >= 0 and len(moves) == count)
        expected_hit = 0 if chip in {'wildcard', 'freehit'} else 4 * max(0, count-allowance)
        _require(row['event_transfers_cost'] == expected_hit)
        if chip != 'freehit':
            for move in moves:
                out, incoming = move['element_out'], move['element_in']
                _require(out in purchases and incoming not in purchases and incoming in by_id)
                cost, sale = _money(move['element_in_cost']), _money(move['element_out_cost'])
                _require(cost > 0 and sale > 0)
                del purchases[out]
                purchases[incoming] = cost
                bank += sale - cost
            # API pairs in one confirmed transfer batch have no funding order.
            _money(bank)
            _require(bank == row['bank'])
        if chip not in {'wildcard', 'freehit'}:
            allowance = min(5, max(0, allowance-count) + 1)
    _require(set(purchases) == _ids(permanent['picks']))
    _require(bank == permanent['entry_history']['bank'])
    _require(permanent['entry_history']['event'] == squad_gw)
    squad = []
    for pid, purchase in sorted(purchases.items()):
        current = _money(by_id[pid]['now_cost'])
        sale = current if current <= purchase else purchase + (current-purchase)//2
        squad.append(dict(element=pid, purchase_price=purchase, selling_price=sale))
    return dict(effective_gameweek=next_gw, bank=bank, free_transfers=allowance,
                squad=squad, baseline=dict(source='public_deadline',
                published_gameweek=published, squad_gameweek=squad_gw,
                note='Unpublished transfers, chips and lineup changes are excluded.'))
