"""Public FPL reads. Never persist partial player-history collections."""
import json
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from urllib.request import Request, urlopen

BASE = 'https://fantasy.premierleague.com/api/'


class FPLClient:
    def get(self, path):
        if path.startswith('/') or '..' in path or '://' in path:
            raise ValueError('Invalid public API path')
        for attempt in range(3):
            try:
                req = Request(BASE + path, headers={'User-Agent': 'fpl-planner/0.1 (public statistics)'})
                with urlopen(req, timeout=20) as response:
                    return json.load(response)
            except (OSError, ValueError):
                if attempt == 2:
                    raise RuntimeError('Public FPL request failed') from None
                time.sleep(0.5 * (attempt + 1))


def completed_events(bootstrap):
    return sorted(e['id'] for e in bootstrap['events']
                  if e.get('finished') and e.get('data_checked'))


def collect(client, bootstrap):
    completed = completed_events(bootstrap)
    fixtures = client.get('fixtures/')
    if len({f['id'] for f in fixtures}) != len(fixtures):
        raise ValueError('Duplicate fixture ID')
    ids = sorted(p['id'] for p in bootstrap['elements'])

    def history(pid):
        records = client.get(f'element-summary/{pid}/')['history']
        return str(pid), [r for r in records if r['round'] in completed]

    with ThreadPoolExecutor(max_workers=3) as pool:
        histories = dict(pool.map(history, ids))
    # Explicit whitelist prevents unrelated account fields ever entering the snapshot.
    fields = ['id', 'web_name', 'element_type', 'team', 'now_cost', 'status',
              'chance_of_playing_next_round', 'penalties_order', 'can_select']
    players = [{k: p[k] for k in fields if k in p} for p in bootstrap['elements']]
    return dict(collected_at=datetime.now(timezone.utc).isoformat(),
                completed=completed, events=bootstrap['events'], teams=bootstrap['teams'],
                players=players, fixtures=fixtures, histories=histories)
