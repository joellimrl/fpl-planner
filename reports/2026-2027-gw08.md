# FPL numerical review after GW8

Data collected: 2026-10-31T13:45:40.120602+00:00. Model: 0.2.0. Forecast events: 10, 11, 12, 13, 14, 15.

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
| Trafford | £5.0m | 4.76 | 25.69 | 77.7 |
| Raya | £6.2m | 4.67 | 25.66 | 77.7 |
| Tzolakis | £4.7m | 3.75 | 24.15 | 77.7 |
| Verbruggen | £4.6m | 3.34 | 21.22 | 77.7 |
| Suzuki | £5.0m | 3.23 | 21.05 | 72.8 |
| Kinsky | £4.4m | 3.26 | 20.17 | 77.7 |
| A.Becker | £5.5m | 3.19 | 19.59 | 77.7 |
| Leno | £4.5m | 3.33 | 19.17 | 77.7 |
| Donnarumma | £5.5m | 3.35 | 17.99 | 77.7 |
| Pickford | £5.5m | 3.52 | 17.24 | 77.7 |
| Roefs | £4.9m | 2.40 | 16.82 | 77.7 |
| Kelleher | £5.0m | 1.94 | 16.53 | 77.7 |
| Lammens | £4.8m | 2.90 | 15.95 | 77.7 |
| Horníček | £5.0m | 2.81 | 15.72 | 77.7 |
| Rushworth | £4.5m | 2.40 | 14.32 | 77.7 |

### Defenders

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Gabriel | £8.0m | 5.41 | 30.40 | 77.7 |
| Vuskovic | £5.2m | 4.25 | 26.69 | 76.5 |
| Muharemović | £5.1m | 4.73 | 25.67 | 77.7 |
| Jacquet | £5.1m | 4.11 | 24.63 | 75.3 |
| Virgil | £6.4m | 4.10 | 24.62 | 77.7 |
| Konsa | £4.7m | 4.39 | 24.52 | 67.7 |
| De Cuyper | £5.3m | 3.88 | 24.44 | 73.1 |
| Tarkowski | £6.2m | 4.80 | 24.31 | 77.7 |
| Hill | £5.5m | 3.91 | 24.21 | 77.7 |
| Egan | £4.1m | 3.44 | 22.97 | 76.3 |
| Van Hecke | £4.9m | 3.53 | 22.55 | 77.7 |
| Silva | £5.0m | 3.69 | 22.43 | 77.7 |
| Bogle | £4.8m | 4.09 | 21.98 | 70.1 |
| Justin | £4.5m | 4.05 | 21.58 | 76.2 |
| Hall | £5.3m | 3.59 | 20.68 | 77.6 |

### Midfielders

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Tavernier | £6.5m | 4.77 | 26.32 | 70.5 |
| Mbeumo | £7.9m | 4.21 | 24.59 | 77.7 |
| Iwobi | £5.4m | 4.15 | 23.00 | 70.3 |
| Tonali | £5.3m | 3.55 | 22.68 | 75.9 |
| Ødegaard | £6.7m | 3.62 | 21.71 | 72.0 |
| Kamara | £5.0m | 3.39 | 21.23 | 77.0 |
| Rayan | £6.3m | 3.83 | 21.12 | 76.0 |
| McAtee | £5.5m | 3.43 | 21.02 | 74.2 |
| Enciso | £5.5m | 3.62 | 20.85 | 69.6 |
| Bobb | £5.5m | 3.74 | 20.76 | 63.9 |
| Groß | £6.2m | 3.36 | 20.42 | 74.8 |
| McGinn | £5.4m | 3.21 | 20.41 | 65.7 |
| Gibbs-White | £7.9m | 3.31 | 20.36 | 64.6 |
| Dewsbury-Hall | £6.6m | 3.86 | 20.36 | 76.8 |
| Cunha | £7.8m | 3.45 | 20.33 | 54.9 |

### Forwards

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Haaland | £15.8m | 5.06 | 30.85 | 76.3 |
| Isak | £9.1m | 4.82 | 27.07 | 59.3 |
| N.Jackson | £6.9m | 3.64 | 23.06 | 65.2 |
| Calvert-Lewin | £6.1m | 3.77 | 22.97 | 74.1 |
| Evanilson | £6.3m | 4.23 | 22.83 | 73.7 |
| Barry | £5.6m | 4.18 | 21.37 | 75.1 |
| Kostoulas | £5.8m | 3.40 | 20.48 | 64.5 |
| Gonzalo | £6.0m | 3.72 | 19.81 | 71.0 |
| Emersonn | £5.5m | 3.28 | 18.64 | 58.3 |
| McBurnie | £5.5m | 2.53 | 17.93 | 76.0 |
| Marmoush | £7.0m | 2.53 | 16.54 | 57.8 |
| Delap | £5.4m | 2.71 | 16.48 | 64.9 |
| Thiago | £7.8m | 2.44 | 16.30 | 77.2 |
| Havertz | £7.4m | 2.64 | 16.27 | 58.0 |
| Thomas-Asante | £5.0m | 2.38 | 15.59 | 54.9 |

## Sources

- https://fantasy.premierleague.com/api/bootstrap-static/
- https://fantasy.premierleague.com/api/fixtures/
- https://fantasy.premierleague.com/api/element-summary/{player_id}/

Run `python -m fpl_planner review --force` to refresh before a deadline. Scheduling is best-effort; there is no automated FPL buying or lineup submission.
