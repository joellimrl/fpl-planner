"""Versioned descriptive forecast. Assumptions are explicit, not backtest claims."""
import math
from collections import defaultdict

DEFAULTS = dict(horizon=6, decay=0.85, prior_minutes=450)
LIMITATIONS = [
    'Uncalibrated v1 statistical model; no demonstrated predictive advantage.',
    'Current availability flags are applied throughout the horizon; return dates are not inferred.',
    'Opponent adjustment uses smoothed match goals, not a fitted xG team model.',
    'xA approximates FPL assists; bonus, saves and threshold probabilities use smoothed historical rates.',
    'Forecasts use complete, data-checked gameweeks only; no cup workload or training news.',
    'Optimiser ignores automatic substitutions and vice-captain fallback; bench points are not counted.',
    'Future prices are held constant; no chip optimisation; max two transfers per gameweek.',
]


def future_events(snapshot, horizon):
    completed = set(snapshot['completed'])
    return sorted(e['id'] for e in snapshot['events'] if e['id'] not in completed)[:horizon]


def _team_rates(snapshot):
    """Count each completed fixture once, not each player's conceded-goals record."""
    rates = defaultdict(lambda: [0, 0, 0])
    for f in snapshot['fixtures']:
        if f.get('event') not in snapshot['completed'] or not f.get('finished'):
            continue
        if f.get('team_h_score') is None or f.get('team_a_score') is None:
            continue
        a, b = f['team_h_score'], f['team_a_score']
        for tid, gf, ga in [(f['team_h'], a, b), (f['team_a'], b, a)]:
            rates[tid][0] += gf; rates[tid][1] += ga; rates[tid][2] += 1
    games = sum(v[2] for v in rates.values())
    mean = sum(v[0] for v in rates.values()) / games if games else 1.4
    mean = max(0.5, mean)
    result = {t['id']: ((rates[t['id']][0] + 6*mean)/(rates[t['id']][2]+6),
                         (rates[t['id']][1] + 6*mean)/(rates[t['id']][2]+6))
              for t in snapshot['teams']}
    return result, mean


def project(snapshot, config):
    cfg = DEFAULTS | config
    if not 1 <= cfg['horizon'] <= 6 or not 0 < cfg['decay'] <= 1 or cfg['prior_minutes'] <= 0:
        raise ValueError('Invalid forecast configuration')
    events = future_events(snapshot, cfg['horizon'])
    last = max(snapshot['completed'], default=0)
    records = {}
    totals = defaultdict(lambda: [0., 0., 0.])
    for p in snapshot['players']:
        rows = [r for r in snapshot['histories'].get(str(p['id']), []) if r['round'] in snapshot['completed']]
        weighted = [(r, cfg['decay'] ** (last-r['round'])) for r in rows]
        records[p['id']] = weighted
        for r, w in weighted:
            totals[p['element_type']][0] += float(r.get('expected_goals', 0))*w
            totals[p['element_type']][1] += float(r.get('expected_assists', 0))*w
            totals[p['element_type']][2] += r.get('minutes', 0)*w/90
    team_rates, league_mean = _team_rates(snapshot)
    result = []
    for p in sorted(snapshot['players'], key=lambda p: p['id']):
        rows = records[p['id']]; pos = p['element_type']
        n = sum(w for _, w in rows)
        def total(field):
            return sum(float(r.get(field, 0))*w for r, w in rows)
        mins = total('minutes'); pseudo = cfg['prior_minutes']/90
        priors = totals[pos]
        xg_prior = priors[0]/priors[2] if priors[2] else (0.01, 0.07, 0.15, 0.25)[pos-1]
        xa_prior = priors[1]/priors[2] if priors[2] else (0.001, 0.05, 0.12, 0.08)[pos-1]
        xg90 = (total('expected_goals')+pseudo*xg_prior)/(mins/90+pseudo)
        xa90 = (total('expected_assists')+pseudo*xa_prior)/(mins/90+pseudo)
        p_play = (sum(w for r,w in rows if r.get('minutes',0)>0)+0.2)/(n+1)
        p_sixty = (sum(w for r,w in rows if r.get('minutes',0)>=60)+0.2)/(n+1)
        emins = (mins+18)/(n+1)
        chance = p.get('chance_of_playing_next_round')
        availability = min(1., max(0., float(chance)/100)) if chance is not None else (0. if p.get('status') in ('i','s','u','n') else 1.)
        threshold = 10 if pos==2 else 12
        def_prob = sum(w for r,w in rows if r.get('minutes',0)>0 and r.get('defensive_contribution',0)>=threshold)/(n+1)
        components = {}
        for event in events:
            parts = dict(appearance=0., goals=0., assists=0., clean_sheet=0., defensive=0., bonus=0., saves=0., deductions=0.)
            for f in snapshot['fixtures']:
                if f.get('event') != event or p['team'] not in (f['team_h'], f['team_a']):
                    continue
                home = f['team_h']==p['team']
                opp = f['team_a'] if home else f['team_h']
                own = team_rates.get(p['team'], (league_mean, league_mean))
                other = team_rates.get(opp, (league_mean, league_mean))
                venue = 1.08 if home else 0.92
                attack_factor = min(1.75,max(0.5,other[1]/league_mean*venue))
                conceded_lambda = min(4.,max(0.2,other[0]*own[1]/league_mean/venue))
                parts['appearance'] += p_play+p_sixty
                parts['goals'] += (10,6,5,4)[pos-1]*xg90*emins/90*attack_factor
                parts['assists'] += 3*xa90*emins/90*attack_factor
                parts['clean_sheet'] += (4,4,1,0)[pos-1]*p_sixty*math.exp(-conceded_lambda)
                parts['defensive'] += 2*def_prob if pos!=1 else 0
                parts['bonus'] += total('bonus')/(n+1)
                parts['saves'] += (sum(math.floor(float(r.get('saves',0))/3)*w for r,w in rows)+5*total('penalties_saved'))/(n+1) if pos==1 else 0
                card_loss = (total('yellow_cards')+3*total('red_cards')+2*total('penalties_missed')+2*total('own_goals'))/(n+1)
                # E[floor(Poisson(lambda)/2)] accounts for the two-goal deduction threshold.
                lam = conceded_lambda*emins/90
                conceded_loss = lam/2-(1-math.exp(-2*lam))/4 if pos in (1,2) else 0
                parts['deductions'] -= card_loss+conceded_loss
            components[event] = {k:round(v*availability,6) for k,v in parts.items()}
        result.append(dict(id=p['id'], name=p['web_name'], position=pos, team=p['team'],
                           price=p['now_cost'], selectable=p.get('can_select',True),
                           forecasts={e:round(sum(v.values()),6) for e,v in components.items()},
                           components=components, expected_minutes=round(emins*availability,2),
                           xg90=round(xg90,4),xa90=round(xa90,4),sample_minutes=round(mins,2)))
    return result
