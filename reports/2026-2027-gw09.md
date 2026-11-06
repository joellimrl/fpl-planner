# FPL numerical review after GW9

Data collected: 2026-11-06T21:39:23.227126+00:00. Model: 0.2.0. Forecast events: 11, 12, 13, 14, 15, 16.

This public report contains league-wide research only, never a private squad or personalised transfer plan.

## Model limitations

- Uncalibrated v1 statistical model; no demonstrated predictive advantage.
- Current availability flags are applied throughout the horizon; return dates are not inferred.
- Opponent adjustment uses smoothed match goals, not a fitted xG team model.
- xA approximates FPL assists; bonus, saves and threshold probabilities use smoothed historical rates.
- Forecasts use complete, data-checked gameweeks only; no cup workload or training news.
- Optimiser ignores automatic substitutions and vice-captain fallback; bench points are not counted.
- Future prices are held constant; no chip optimisation; max two transfers per gameweek.

## Retrospective forecast check

Retrospective check of historical rows, not a decision backtest: current player clubs/positions and current data revisions can leak metadata. Historical injuries, prices and squad finances are unavailable. Availability is neutralised. No predictive superiority is claimed.

Observations: 825; model MAE: 2.1321; four-week points-average MAE: 2.3994. Lower error is better; this is not an unbiased strategy comparison.

## Rankings by position

Projected points are model estimates, not guarantees. All horizon totals are unmultiplied player points; they are not squad gains.

### Goalkeepers

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Verbruggen | £4.6m | 4.22 | 26.21 | 78.2 |
| Trafford | £5.0m | 3.51 | 24.33 | 78.2 |
| Raya | £6.2m | 3.96 | 23.85 | 78.2 |
| Tzolakis | £4.7m | 3.04 | 21.80 | 78.2 |
| Kinsky | £4.4m | 3.18 | 19.82 | 78.2 |
| A.Becker | £5.5m | 3.39 | 19.59 | 78.2 |
| Kelleher | £5.0m | 3.55 | 19.17 | 78.2 |
| Pickford | £5.5m | 2.68 | 18.48 | 78.2 |
| Suzuki | £5.0m | 3.56 | 18.40 | 74.2 |
| Leno | £4.5m | 2.43 | 18.40 | 78.2 |
| Donnarumma | £5.5m | 3.35 | 17.55 | 78.2 |
| Lammens | £4.8m | 2.74 | 16.66 | 78.2 |
| Roefs | £4.9m | 2.57 | 16.50 | 78.2 |
| Horníček | £5.0m | 2.74 | 15.80 | 78.2 |
| Petrović | £4.5m | 3.19 | 15.24 | 78.2 |

### Defenders

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Gabriel | £8.0m | 4.87 | 29.09 | 78.2 |
| Van Hecke | £5.0m | 4.97 | 28.13 | 78.2 |
| Konsa | £4.8m | 4.69 | 28.07 | 70.1 |
| Vuskovic | £5.2m | 4.10 | 26.27 | 77.3 |
| Muharemović | £5.1m | 3.71 | 25.56 | 78.2 |
| De Cuyper | £5.4m | 3.89 | 25.22 | 71.4 |
| Silva | £5.1m | 4.80 | 24.42 | 78.2 |
| Jacquet | £5.1m | 4.18 | 23.93 | 76.3 |
| Hill | £5.6m | 4.67 | 23.84 | 78.2 |
| Tarkowski | £6.2m | 3.46 | 23.33 | 78.2 |
| Virgil | £6.4m | 4.06 | 23.20 | 78.2 |
| Ajer | £4.5m | 3.98 | 21.84 | 78.2 |
| Araujo | £5.4m | 3.73 | 21.45 | 61.2 |
| Murillo | £5.5m | 3.36 | 21.44 | 78.2 |
| Justin | £4.5m | 3.01 | 21.30 | 75.9 |

### Midfielders

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Tavernier | £6.6m | 4.52 | 25.10 | 72.4 |
| Rice | £7.4m | 4.00 | 23.69 | 74.7 |
| Iwobi | £5.4m | 3.73 | 23.34 | 69.7 |
| E.Le Fée | £5.7m | 3.64 | 22.94 | 75.0 |
| McAtee | £5.5m | 3.59 | 21.89 | 75.4 |
| Tonali | £5.3m | 3.94 | 21.80 | 76.8 |
| Mbeumo | £7.9m | 3.27 | 21.60 | 78.2 |
| Ayari | £5.4m | 3.32 | 21.50 | 68.6 |
| Enciso | £5.5m | 3.42 | 21.45 | 71.7 |
| Rudoni | £4.9m | 4.07 | 21.27 | 68.3 |
| Ødegaard | £6.7m | 3.60 | 21.21 | 73.1 |
| Dewsbury-Hall | £6.6m | 3.29 | 20.82 | 77.5 |
| Rogers | £8.2m | 3.28 | 20.78 | 76.9 |
| Rayan | £6.3m | 3.73 | 20.60 | 76.4 |
| Xhaka | £5.4m | 3.32 | 20.59 | 78.2 |

### Forwards

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Haaland | £15.8m | 5.04 | 28.84 | 77.1 |
| N.Jackson | £7.0m | 4.46 | 25.58 | 68.0 |
| Evanilson | £6.4m | 4.45 | 25.28 | 72.6 |
| Isak | £9.2m | 4.44 | 25.04 | 63.3 |
| Barry | £5.6m | 3.92 | 24.79 | 74.3 |
| McBurnie | £5.5m | 3.23 | 20.78 | 76.9 |
| Havertz | £7.4m | 3.45 | 20.28 | 61.1 |
| Thiago | £7.8m | 3.29 | 20.13 | 77.9 |
| Kostoulas | £5.8m | 3.05 | 19.77 | 64.5 |
| Gonzalo | £5.9m | 3.01 | 18.48 | 72.2 |
| Emersonn | £5.5m | 2.81 | 17.70 | 60.2 |
| Marmoush | £7.0m | 3.16 | 16.71 | 59.8 |
| Calvert-Lewin | £6.1m | 2.76 | 16.59 | 56.5 |
| Brobbey | £5.7m | 2.62 | 16.43 | 52.5 |
| Delap | £5.4m | 2.68 | 16.23 | 63.6 |

## Sources

- https://fantasy.premierleague.com/api/bootstrap-static/
- https://fantasy.premierleague.com/api/fixtures/
- https://fantasy.premierleague.com/api/element-summary/{player_id}/

Run `python -m fpl_planner review --force` to refresh before a deadline. Scheduling is best-effort; there is no automated FPL buying or lineup submission.
