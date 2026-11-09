# FPL numerical review after GW10

Data collected: 2026-11-09T22:34:01.727237+00:00. Model: 0.2.0. Forecast events: 11, 12, 13, 14, 15, 16.

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

Observations: 863; model MAE: 2.0474; four-week points-average MAE: 2.2749. Lower error is better; this is not an unbiased strategy comparison.

## Rankings by position

Projected points are model estimates, not guarantees. All horizon totals are unmultiplied player points; they are not squad gains.

### Goalkeepers

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Trafford | £5.0m | 4.11 | 27.32 | 78.7 |
| Verbruggen | £4.6m | 4.18 | 25.10 | 78.7 |
| Tzolakis | £4.7m | 3.49 | 24.37 | 78.7 |
| Raya | £6.2m | 3.91 | 23.44 | 78.7 |
| A.Becker | £5.5m | 3.43 | 20.95 | 78.7 |
| Kinsky | £4.4m | 3.12 | 19.29 | 78.7 |
| Roefs | £4.9m | 2.82 | 19.00 | 78.7 |
| Kelleher | £5.0m | 3.39 | 18.89 | 78.7 |
| Leno | £4.5m | 2.54 | 18.82 | 78.7 |
| Pickford | £5.5m | 2.88 | 18.58 | 78.7 |
| Donnarumma | £5.4m | 3.15 | 16.63 | 78.7 |
| Suzuki | £5.0m | 3.27 | 16.61 | 75.4 |
| Horníček | £5.0m | 2.86 | 16.26 | 78.7 |
| Lammens | £4.8m | 2.47 | 15.94 | 78.7 |
| Petrović | £4.5m | 2.98 | 15.24 | 78.7 |

### Defenders

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Gabriel | £8.1m | 5.00 | 30.00 | 78.7 |
| Konsa | £4.8m | 4.86 | 29.15 | 72.0 |
| Muharemović | £5.1m | 4.31 | 28.63 | 78.7 |
| Van Hecke | £5.1m | 5.04 | 28.39 | 78.7 |
| Vuskovic | £5.3m | 4.59 | 28.29 | 77.9 |
| De Cuyper | £5.5m | 4.15 | 26.13 | 71.6 |
| Jacquet | £5.1m | 4.32 | 25.45 | 77.1 |
| Hill | £5.6m | 4.73 | 25.34 | 78.7 |
| Justin | £4.5m | 3.60 | 24.38 | 76.8 |
| Araujo | £5.5m | 4.19 | 24.12 | 64.7 |
| Silva | £5.1m | 4.50 | 23.92 | 78.7 |
| Murillo | £5.5m | 3.53 | 22.63 | 78.6 |
| Bogle | £4.8m | 3.29 | 22.56 | 73.6 |
| Tarkowski | £6.2m | 3.40 | 21.81 | 78.7 |
| Ajer | £4.5m | 3.84 | 21.71 | 78.7 |

### Midfielders

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| E.Le Fée | £5.7m | 4.39 | 26.82 | 75.6 |
| Tavernier | £6.7m | 4.54 | 25.52 | 73.9 |
| Ødegaard | £6.7m | 4.10 | 24.61 | 74.5 |
| Groß | £6.3m | 3.65 | 23.92 | 76.7 |
| Rice | £7.5m | 3.80 | 22.82 | 71.3 |
| Dewsbury-Hall | £6.6m | 3.59 | 22.25 | 78.1 |
| Iwobi | £5.4m | 3.63 | 22.19 | 71.6 |
| McGinn | £5.4m | 3.78 | 21.64 | 67.0 |
| Wirtz | £7.2m | 3.89 | 21.39 | 69.9 |
| Mbeumo | £7.9m | 3.18 | 21.37 | 77.4 |
| Kamara | £5.0m | 3.67 | 21.26 | 76.6 |
| Rudoni | £4.9m | 4.07 | 21.12 | 69.8 |
| Ayari | £5.5m | 3.29 | 21.12 | 68.8 |
| Rogers | £8.2m | 3.19 | 20.79 | 77.6 |
| Gomez | £5.0m | 3.27 | 20.78 | 76.5 |

### Forwards

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| N.Jackson | £7.1m | 4.90 | 28.76 | 69.5 |
| Evanilson | £6.5m | 4.87 | 27.77 | 73.1 |
| Barry | £5.7m | 4.46 | 27.76 | 75.5 |
| Haaland | £15.8m | 4.75 | 27.11 | 77.8 |
| Isak | £9.3m | 4.85 | 26.29 | 66.5 |
| Calvert-Lewin | £6.0m | 3.63 | 22.23 | 76.3 |
| McBurnie | £5.5m | 3.02 | 19.86 | 77.6 |
| Havertz | £7.4m | 3.25 | 19.49 | 60.2 |
| Kostoulas | £5.8m | 2.99 | 19.45 | 66.0 |
| Delap | £5.3m | 3.18 | 19.14 | 66.0 |
| Gonzalo | £5.9m | 3.01 | 17.86 | 69.8 |
| Brobbey | £5.7m | 2.77 | 16.72 | 53.8 |
| Marmoush | £7.0m | 3.15 | 16.47 | 59.5 |
| Emersonn | £5.4m | 2.55 | 16.21 | 58.1 |
| Wissa | £5.9m | 1.98 | 14.03 | 55.2 |

## Sources

- https://fantasy.premierleague.com/api/bootstrap-static/
- https://fantasy.premierleague.com/api/fixtures/
- https://fantasy.premierleague.com/api/element-summary/{player_id}/

Run `python -m fpl_planner review --force` to refresh before a deadline. Scheduling is best-effort; there is no automated FPL buying or lineup submission.
