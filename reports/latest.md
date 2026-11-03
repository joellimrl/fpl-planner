# FPL numerical review after GW9

Data collected: 2026-11-03T17:57:16.267767+00:00. Model: 0.2.0. Forecast events: 10, 11, 12, 13, 14, 15.

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
| Verbruggen | £4.6m | 4.10 | 26.06 | 78.2 |
| Trafford | £5.0m | 4.47 | 24.24 | 78.2 |
| Raya | £6.2m | 4.29 | 23.77 | 78.2 |
| Tzolakis | £4.7m | 3.42 | 22.22 | 78.2 |
| Kinsky | £4.4m | 3.34 | 20.00 | 78.2 |
| A.Becker | £5.5m | 3.23 | 19.43 | 78.2 |
| Suzuki | £5.0m | 3.01 | 19.08 | 74.2 |
| Pickford | £5.5m | 3.53 | 18.43 | 78.2 |
| Leno | £4.5m | 3.31 | 18.40 | 78.2 |
| Kelleher | £5.0m | 2.19 | 18.07 | 78.2 |
| Donnarumma | £5.5m | 3.40 | 17.78 | 78.2 |
| Lammens | £4.8m | 3.12 | 17.30 | 78.2 |
| Horníček | £5.0m | 2.91 | 16.41 | 78.2 |
| Roefs | £4.9m | 2.14 | 15.68 | 78.2 |
| Rushworth | £4.5m | 2.40 | 14.60 | 78.2 |

### Defenders

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Gabriel | £8.0m | 5.14 | 28.81 | 78.2 |
| Van Hecke | £5.0m | 4.49 | 28.27 | 78.2 |
| Konsa | £4.7m | 4.94 | 27.89 | 70.1 |
| Vuskovic | £5.2m | 4.04 | 25.83 | 77.3 |
| Muharemović | £5.1m | 4.63 | 25.44 | 78.2 |
| De Cuyper | £5.4m | 3.85 | 24.70 | 71.4 |
| Jacquet | £5.1m | 4.05 | 23.89 | 76.3 |
| Silva | £5.0m | 3.82 | 23.64 | 78.2 |
| Tarkowski | £6.2m | 4.45 | 23.38 | 78.2 |
| Virgil | £6.4m | 3.92 | 23.15 | 78.2 |
| Hill | £5.5m | 3.66 | 23.08 | 78.2 |
| Araujo | £5.4m | 3.63 | 21.44 | 61.2 |
| Branthwaite | £5.5m | 4.02 | 21.23 | 64.3 |
| Justin | £4.5m | 3.91 | 21.18 | 75.9 |
| Bogle | £4.8m | 3.79 | 20.61 | 72.1 |

### Midfielders

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Tavernier | £6.6m | 4.51 | 24.81 | 72.4 |
| Iwobi | £5.4m | 4.41 | 23.99 | 69.7 |
| Rice | £7.4m | 3.98 | 23.41 | 74.7 |
| Mbeumo | £7.9m | 3.86 | 22.51 | 78.2 |
| E.Le Fée | £5.7m | 3.98 | 22.34 | 75.0 |
| Enciso | £5.5m | 3.78 | 22.09 | 71.7 |
| Tonali | £5.3m | 3.45 | 21.80 | 76.8 |
| McAtee | £5.5m | 3.58 | 21.79 | 75.4 |
| Dewsbury-Hall | £6.6m | 3.98 | 21.21 | 77.5 |
| Rudoni | £4.9m | 3.14 | 21.13 | 68.3 |
| Ayari | £5.4m | 3.40 | 20.96 | 68.6 |
| Ødegaard | £6.7m | 3.56 | 20.86 | 73.1 |
| Rogers | £8.1m | 3.63 | 20.80 | 76.9 |
| Bobb | £5.5m | 3.80 | 20.68 | 65.1 |
| Neto | £6.6m | 3.54 | 20.41 | 70.5 |

### Forwards

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Haaland | £15.8m | 4.82 | 28.73 | 77.1 |
| N.Jackson | £7.0m | 4.08 | 25.58 | 68.0 |
| Barry | £5.6m | 4.97 | 25.56 | 74.3 |
| Isak | £9.2m | 4.56 | 25.53 | 63.3 |
| Evanilson | £6.4m | 4.64 | 25.11 | 72.6 |
| Calvert-Lewin | £6.1m | 3.55 | 22.04 | 75.4 |
| McBurnie | £5.5m | 2.96 | 20.49 | 76.9 |
| Havertz | £7.4m | 3.34 | 19.95 | 61.1 |
| Gonzalo | £5.9m | 3.65 | 19.26 | 72.2 |
| Thiago | £7.8m | 2.91 | 19.22 | 77.9 |
| Kostoulas | £5.8m | 3.15 | 19.22 | 64.5 |
| Emersonn | £5.5m | 3.15 | 18.19 | 60.2 |
| Marmoush | £7.0m | 2.57 | 16.67 | 59.8 |
| Delap | £5.4m | 2.69 | 16.29 | 63.6 |
| Brobbey | £5.7m | 2.94 | 16.05 | 52.5 |

## Sources

- https://fantasy.premierleague.com/api/bootstrap-static/
- https://fantasy.premierleague.com/api/fixtures/
- https://fantasy.premierleague.com/api/element-summary/{player_id}/

Run `python -m fpl_planner review --force` to refresh before a deadline. Scheduling is best-effort; there is no automated FPL buying or lineup submission.
