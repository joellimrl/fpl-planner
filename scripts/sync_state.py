"""Upload a local FPL export to Actions Secrets. Never print its contents."""
import argparse
import json
import subprocess
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--repo',required=True)
parser.add_argument('--input',type=Path,required=True,help='Private state JSON or FPL my-team export')
parser.add_argument('--gameweek',type=int,required=True)
args=parser.parse_args()
raw=json.loads(args.input.read_text(encoding='utf-8'))
if 'picks' in raw:
    state=dict(effective_gameweek=args.gameweek,bank=raw['transfers']['bank'],
               free_transfers=max(0,raw['transfers']['limit']-raw['transfers']['made']),
               squad=[{k:p[k] for k in ('element','purchase_price','selling_price')} for p in raw['picks']])
else:state=raw
if state.get('effective_gameweek')!=args.gameweek:
    raise SystemExit('State gameweek mismatch')
result=subprocess.run(['gh','secret','set','FPL_TEAM_STATE','--repo',args.repo],
                       input=json.dumps(state).encode(),capture_output=True)
if result.returncode:raise SystemExit('Secret update failed; check GitHub CLI authentication')
print('Private squad state updated in GitHub Actions Secrets.')
