# FPL numerical review after GW8

Data collected: 2026-10-28T05:58:13.114950+00:00. Model: 0.2.0. Forecast events: 9, 10, 11, 12, 13, 14.

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

Observations: 779; model MAE: 2.201; four-week points-average MAE: 2.5231. Lower error is better; this is not an unbiased strategy comparison.

## Rankings by position

Projected points are model estimates, not guarantees. All horizon totals are unmultiplied player points; they are not squad gains.

### Goalkeepers

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Trafford | £5.0m | 4.15 | 25.61 | 77.7 |
| Raya | £6.2m | 4.25 | 25.48 | 77.7 |
| Tzolakis | £4.7m | 4.10 | 23.80 | 77.7 |
| Suzuki | £5.0m | 3.67 | 21.10 | 72.8 |
| Kinsky | £4.4m | 3.53 | 20.44 | 77.7 |
| Verbruggen | £4.6m | 2.64 | 20.01 | 77.7 |
| Leno | £4.5m | 3.33 | 19.34 | 77.7 |
| A.Becker | £5.5m | 3.11 | 19.24 | 77.7 |
| Pickford | £5.5m | 2.68 | 18.00 | 77.7 |
| Donnarumma | £5.5m | 2.28 | 17.62 | 77.7 |
| Kelleher | £5.0m | 3.55 | 17.00 | 77.7 |
| Roefs | £4.9m | 3.11 | 16.55 | 77.7 |
| Horníček | £5.0m | 3.09 | 16.38 | 77.7 |
| Lammens | £4.8m | 1.95 | 15.28 | 77.7 |
| Rushworth | £4.5m | 2.90 | 14.65 | 77.7 |

### Defenders

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Gabriel | £7.9m | 4.87 | 29.87 | 77.7 |
| Muharemović | £5.1m | 4.12 | 25.70 | 77.7 |
| Vuskovic | £5.2m | 3.46 | 25.40 | 76.5 |
| Tarkowski | £6.2m | 3.88 | 25.17 | 77.7 |
| Hill | £5.5m | 4.35 | 24.91 | 77.7 |
| Jacquet | £5.1m | 3.83 | 24.27 | 75.3 |
| Virgil | £6.4m | 3.84 | 24.25 | 77.7 |
| Konsa | £4.7m | 3.97 | 24.17 | 67.7 |
| Van Hecke | £4.9m | 4.22 | 23.19 | 77.7 |
| Silva | £5.0m | 4.02 | 23.19 | 77.7 |
| De Cuyper | £5.3m | 3.09 | 23.16 | 73.1 |
| Egan | £4.1m | 4.03 | 22.72 | 76.3 |
| Bogle | £4.8m | 3.49 | 22.08 | 70.1 |
| Justin | £4.5m | 3.44 | 21.60 | 76.2 |
| Hall | £5.3m | 3.91 | 21.26 | 77.6 |

### Midfielders

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Tavernier | £6.4m | 4.26 | 26.71 | 70.5 |
| Mbeumo | £7.9m | 4.02 | 24.18 | 77.7 |
| Tonali | £5.3m | 4.28 | 23.34 | 75.9 |
| Iwobi | £5.4m | 3.83 | 23.03 | 70.3 |
| Rayan | £6.3m | 3.42 | 21.46 | 76.0 |
| Kamara | £5.0m | 3.48 | 21.19 | 77.0 |
| Ødegaard | £6.7m | 3.35 | 21.12 | 72.0 |
| Dewsbury-Hall | £6.6m | 3.45 | 20.81 | 76.8 |
| Bobb | £5.5m | 3.46 | 20.79 | 63.9 |
| McAtee | £5.5m | 3.33 | 20.69 | 74.2 |
| Enciso | £5.5m | 3.17 | 20.33 | 69.6 |
| McGinn | £5.4m | 3.29 | 20.33 | 65.7 |
| E.Le Fée | £5.7m | 3.51 | 20.21 | 73.7 |
| Neto | £6.6m | 3.48 | 20.19 | 68.9 |
| Stach | £6.0m | 3.26 | 20.14 | 66.1 |

### Forwards

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Haaland | £15.8m | 5.03 | 29.90 | 76.3 |
| Isak | £9.1m | 4.04 | 27.00 | 59.3 |
| Calvert-Lewin | £6.1m | 3.75 | 23.33 | 74.1 |
| Evanilson | £6.2m | 3.62 | 23.11 | 73.7 |
| N.Jackson | £6.8m | 3.65 | 22.95 | 65.2 |
| Barry | £5.6m | 3.75 | 21.97 | 75.1 |
| Kostoulas | £5.8m | 3.22 | 20.30 | 64.5 |
| Gonzalo | £6.0m | 3.27 | 19.81 | 71.0 |
| McBurnie | £5.5m | 3.50 | 18.37 | 76.0 |
| Emersonn | £5.5m | 2.81 | 18.11 | 58.3 |
| Marmoush | £7.0m | 3.27 | 17.20 | 57.8 |
| Thiago | £7.8m | 2.97 | 16.56 | 77.2 |
| Delap | £5.5m | 2.51 | 16.15 | 64.9 |
| Havertz | £7.5m | 2.49 | 15.80 | 58.0 |
| Thomas-Asante | £5.0m | 2.73 | 15.68 | 54.9 |

## Sources

- https://fantasy.premierleague.com/api/bootstrap-static/
- https://fantasy.premierleague.com/api/fixtures/
- https://fantasy.premierleague.com/api/element-summary/{player_id}/

Run `python -m fpl_planner review --force` to refresh before a deadline. Scheduling is best-effort; there is no automated FPL buying or lineup submission.
