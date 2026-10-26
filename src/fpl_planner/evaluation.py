"""Limited retrospective forecast check, explicitly not a strategy backtest."""
from copy import deepcopy
from .forecast import project

CAVEAT = ('Retrospective check of historical rows, not a decision backtest: current player clubs/positions '
          'and current data revisions can leak metadata. Historical injuries, prices and squad finances '
          'are unavailable. Availability is neutralised. No predictive superiority is claimed.')


def evaluate(snapshot,config):
    errors=[];baseline_errors=[];weeks=[]
    for event in sorted(snapshot['completed'])[-3:]:
        past=[e for e in snapshot['completed'] if e<event]
        if len(past)<3:continue
        train=deepcopy(snapshot);train['completed']=past
        train['events']=[dict(e,is_next=e['id']==event) for e in snapshot['events']]
        train['histories']={pid:[r for r in rows if r['round']<event] for pid,rows in snapshot['histories'].items()}
        for p in train['players']:
            p['status']='a';p['chance_of_playing_next_round']=None
        forecasts=project(train,config|{'horizon':1})
        for p in forecasts:
            prior=train['histories'].get(str(p['id']),[])
            actual=[r for r in snapshot['histories'].get(str(p['id']),[]) if r['round']==event]
            if sum(r.get('minutes',0) for r in prior)<180 or not actual:continue
            # Fixtures, not rows, determine games/week for double-gameweek baselines.
            distinct=sorted({r['round'] for r in prior})[-4:]
            per_week=[sum(r.get('total_points',0) for r in prior if r['round']==g) for g in distinct]
            baseline=sum(per_week)/len(per_week)
            predicted=p['forecasts'].get(event,0)
            outcome=sum(r.get('total_points',0) for r in actual)
            errors.append(abs(predicted-outcome));baseline_errors.append(abs(baseline-outcome))
        weeks.append(event)
    return dict(observations=len(errors),gameweeks=weeks,
                model_mae=round(sum(errors)/len(errors),4) if errors else None,
                baseline_mae=round(sum(baseline_errors)/len(baseline_errors),4) if errors else None,
                caveat=CAVEAT)
