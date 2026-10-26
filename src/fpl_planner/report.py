"""Public research reports and encrypted personal output; no private console logs."""
import gzip
import hashlib
import json
import os
import tempfile
from pathlib import Path
from . import __version__
from .data import collect, completed_events
from .forecast import LIMITATIONS, future_events, project
from .optimise import compare
from .privacy import canonical, fingerprint, seal
from .state import validate_state
from .evaluation import evaluate


def _text(value):
    return str(value).replace('|','/').replace('\n',' ').replace('<','&lt;').replace('>','&gt;')


def public_markdown(snapshot,players,config):
    events=future_events(snapshot,config.get('horizon',6))
    last=max(snapshot['completed'])
    lines=[f'# FPL numerical review after GW{last}', '',
           f"Data collected: {snapshot['collected_at']}. Model: {__version__}. Forecast events: {', '.join(map(str,events))}.",
           '', 'This public report contains league-wide research only, never a private squad or personalised transfer plan.',
           '', '## Model limitations', '']
    lines.extend('- '+v for v in LIMITATIONS)
    check=evaluate(snapshot,config)
    lines.extend(['','## Retrospective forecast check','',check['caveat'], '',
                  f"Observations: {check['observations']}; model MAE: {check['model_mae']}; four-week points-average MAE: {check['baseline_mae']}. Lower error is better; this is not an unbiased strategy comparison."])
    lines.extend(['','## Rankings by position','',
                  'Projected points are model estimates, not guarantees. All horizon totals are unmultiplied player points; they are not squad gains.'])
    for pos,title in [(1,'Goalkeepers'),(2,'Defenders'),(3,'Midfielders'),(4,'Forwards')]:
        lines.extend(['',f'### {title}','','| Player | Price | Next GW | Horizon | Expected minutes/match |','|---|---:|---:|---:|---:|'])
        ranked=sorted((p for p in players if p['position']==pos and p.get('selectable',True)),
                      key=lambda p:(-sum(p['forecasts'].values()),p['id']))[:15]
        for p in ranked:
            lines.append(f"| {_text(p['name'])} | £{p['price']/10:.1f}m | {p['forecasts'].get(events[0],0):.2f} | {sum(p['forecasts'].values()):.2f} | {p['expected_minutes']:.1f} |")
    lines.extend(['','## Sources','',
                  '- https://fantasy.premierleague.com/api/bootstrap-static/',
                  '- https://fantasy.premierleague.com/api/fixtures/',
                  '- https://fantasy.premierleague.com/api/element-summary/{player_id}/',
                  '', 'Run `python -m fpl_planner review --force` to refresh before a deadline. Scheduling is best-effort; there is no automated FPL buying or lineup submission.',''])
    return '\n'.join(lines)


def personal_markdown(report):
    """Render only locally, after authenticated decryption."""
    lookup={int(k):v for k,v in report['players'].items()}
    comparison=report['comparison'];best=comparison['best'];hold=comparison['hold']
    names=lambda ids:', '.join(_text(lookup.get(i,i)) for i in ids) or 'None'
    lines=['# Personal FPL numerical plan','',f"Snapshot: {report['collected_at']}; model {report['model']}",
           '',f"Best incumbent plan: {best['objective']:.2f} net points; wait-now incumbent: {hold['objective']:.2f}.",
           f"Incumbent difference: {comparison['gain']:.2f}; solver-bound interval: {comparison['gain_interval']}.",
           f"Solver status: {best['status']}; relative gap: {best['gap']}. A positive incumbent difference alone is not proof of a better first action when bounds overlap."]
    for week in best['weeks']:
        lines.extend(['',f"## Gameweek {week['event']}",'',f"Sell: {names(week['sells'])}",
                      f"Buy: {names(week['buys'])}",f"Hit: {week['hit']} points. Bank: £{week['bank']/10:.1f}m. Free transfers next week: {week['next_free_transfers']}.",
                      f"Projected scoring points: {week['scoring_points']:.2f} before this week's hit.",
                      '',f"Starting XI: {names(week['starters'])}",
                      f"Captain: {names([week['captain']])}; vice: {names([week['vice_captain']])}",
                      f"Bench (outfield order followed by goalkeeper): {names(week['bench'])}"])
    lines.extend(['','## Limitations','']+['- '+v for v in report['limitations']])
    return '\n'.join(lines)+'\n'


def run_review(root,client,state=None,key=None,force=False):
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    config_path=root/'config/model.json'
    config=json.loads(config_path.read_text()) if config_path.exists() else {'horizon':6}
    boot=client.get('bootstrap-static/')
    complete=completed_events(boot)
    if not complete:return {'status':'no_completed_gameweek'}
    first=next((e for e in boot['events'] if e['id']==1),{})
    year=first.get('deadline_time','unknown')[:4]
    season=f'{year}-{int(year)+1}' if year.isdigit() else 'unknown'
    marker=dict(season=season,completed=max(complete),model=__version__,
                config=hashlib.sha256(canonical(config)).hexdigest(),
                private=fingerprint(state,key) if state is not None and key else None)
    manifest=root/'data/manifest.json'
    if manifest.exists() and not force:
        old=json.loads(manifest.read_text())
        if all(old.get(k)==v for k,v in marker.items()):return {'status':'unchanged'}
    snap=collect(client,boot)
    players=project(snap,config)
    events=future_events(snap,config.get('horizon',6))
    if not events:return {'status':'season_complete'}
    personal_status='not_configured';private_cipher=None
    if state is not None and key:
        try:validated=validate_state(state,players,events[0])
        except ValueError:personal_status='state_refresh_required'
        else:
            plans=compare(players,validated,events,config)
            report=dict(collected_at=snap['collected_at'],model=__version__,events=events,
                        state_effective_gameweek=validated['effective_gameweek'],
                        comparison=plans,players={p['id']:p['name'] for p in players},
                        limitations=LIMITATIONS)
            private_cipher=seal(report,key);personal_status='encrypted'
    elif state is not None:personal_status='encryption_key_required'
    label=f'{season}-gw{max(complete):02d}'
    files={f'data/snapshots/{label}.json.gz':gzip.compress(canonical(snap),mtime=0),
           f'data/forecasts/{label}.json.gz':gzip.compress(canonical(players),mtime=0),
           f'reports/{label}.md':public_markdown(snap,players,config).encode(),
           'reports/latest.md':public_markdown(snap,players,config).encode()}
    if private_cipher:
        files[f'reports/private/{label}.enc']=private_cipher
        files['reports/private/latest.enc']=private_cipher
    marker['personal_status']=personal_status
    # The final marker is written last. Actions commits only on success, with one writer.
    files['data/manifest.json']=canonical(marker)+b'\n'
    with tempfile.TemporaryDirectory(prefix='.publish-',dir=root) as tmp:
        staged=Path(tmp)
        for name,data in files.items():
            dest=staged/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
        for name in files:
            dest=root/name;dest.parent.mkdir(parents=True,exist_ok=True)
            os.replace(staged/name,dest)
    return dict(status='generated',completed=max(complete),personal=personal_status,players=len(players))
