# FPL numerical review after GW10

Data collected: 2026-11-22T00:30:44.979183+00:00. Model: 0.2.0. Forecast events: 12, 13, 14, 15, 16, 17.

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
| Trafford | £5.1m | 5.05 | 27.67 | 78.7 |
| Verbruggen | £4.7m | 4.28 | 25.19 | 78.7 |
| Tzolakis | £4.7m | 4.32 | 25.13 | 78.7 |
| A.Becker | £5.5m | 3.31 | 20.92 | 78.7 |
| Pickford | £5.5m | 3.31 | 19.51 | 78.7 |
| Kinsky | £4.4m | 3.45 | 19.22 | 78.7 |
| Roefs | £4.8m | 3.45 | 19.16 | 78.7 |
| Leno | £4.5m | 3.16 | 18.82 | 78.7 |
| Kelleher | £5.0m | 2.96 | 18.38 | 78.7 |
| Raya | £6.3m | 2.74 | 17.76 | 59.0 |
| Lammens | £4.8m | 2.60 | 16.68 | 78.7 |
| Suzuki | £5.1m | 2.40 | 16.42 | 75.4 |
| Donnarumma | £5.4m | 2.45 | 16.10 | 78.7 |
| Horníček | £5.0m | 1.88 | 15.85 | 78.7 |
| Petrović | £4.5m | 2.61 | 14.87 | 78.7 |

### Defenders

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Gabriel | £8.1m | 4.76 | 30.45 | 78.7 |
| Konsa | £4.9m | 4.64 | 29.50 | 72.0 |
| Muharemović | £5.1m | 5.38 | 29.00 | 78.7 |
| Vuskovic | £5.3m | 4.91 | 28.40 | 77.9 |
| Van Hecke | £5.2m | 5.07 | 28.05 | 78.7 |
| De Cuyper | £5.5m | 4.61 | 26.25 | 71.6 |
| Jacquet | £5.1m | 3.95 | 25.18 | 77.1 |
| Hill | £5.6m | 4.26 | 24.86 | 78.7 |
| Justin | £4.5m | 4.70 | 24.75 | 76.8 |
| Virgil | £6.4m | 3.80 | 24.24 | 78.7 |
| Araujo | £5.5m | 3.70 | 23.73 | 64.7 |
| Silva | £5.1m | 4.02 | 23.42 | 78.7 |
| Bogle | £4.8m | 4.44 | 22.94 | 73.6 |
| Murillo | £5.5m | 3.77 | 22.92 | 78.6 |
| Tarkowski | £6.2m | 3.85 | 22.85 | 78.7 |

### Midfielders

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| E.Le Fée | £5.7m | 4.31 | 26.35 | 75.6 |
| Ødegaard | £6.7m | 4.09 | 25.10 | 74.5 |
| Tavernier | £6.7m | 4.15 | 25.06 | 73.9 |
| Groß | £6.3m | 4.28 | 24.00 | 76.7 |
| Rice | £7.5m | 3.78 | 23.19 | 71.3 |
| Dewsbury-Hall | £6.7m | 3.76 | 22.90 | 78.1 |
| Iwobi | £5.4m | 3.99 | 22.02 | 71.6 |
| Mbeumo | £7.8m | 3.48 | 21.92 | 77.4 |
| Rogers | £8.3m | 3.28 | 21.19 | 77.6 |
| Ayari | £5.5m | 3.73 | 21.18 | 68.8 |
| McGinn | £5.5m | 3.56 | 20.97 | 67.0 |
| Kamara | £5.0m | 3.48 | 20.96 | 76.6 |
| Gomez | £5.1m | 3.64 | 20.83 | 76.5 |
| Wirtz | £7.3m | 3.26 | 20.83 | 69.9 |
| Rudoni | £4.9m | 2.98 | 20.56 | 69.8 |

### Forwards

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Barry | £5.7m | 4.66 | 28.72 | 75.5 |
| N.Jackson | £7.2m | 4.80 | 28.04 | 69.5 |
| Evanilson | £6.6m | 4.51 | 27.33 | 73.1 |
| Haaland | £15.8m | 3.85 | 27.15 | 77.8 |
| Isak | £9.3m | 4.01 | 25.51 | 66.5 |
| Calvert-Lewin | £6.0m | 4.12 | 22.29 | 76.3 |
| McBurnie | £5.5m | 3.75 | 20.04 | 77.6 |
| Havertz | £7.4m | 3.28 | 19.87 | 60.2 |
| Kostoulas | £5.8m | 3.45 | 19.50 | 66.0 |
| Delap | £5.3m | 3.52 | 19.41 | 66.0 |
| Gonzalo | £5.8m | 3.30 | 17.66 | 69.8 |
| Emersonn | £5.4m | 3.00 | 16.35 | 58.1 |
| Marmoush | £7.0m | 2.85 | 16.20 | 59.5 |
| Wissa | £5.9m | 1.97 | 14.47 | 55.2 |
| Thomas-Asante | £5.0m | 1.89 | 12.93 | 42.4 |

## Sources

- https://fantasy.premierleague.com/api/bootstrap-static/
- https://fantasy.premierleague.com/api/fixtures/
- https://fantasy.premierleague.com/api/element-summary/{player_id}/

Run `python -m fpl_planner review --force` to refresh before a deadline. Scheduling is best-effort; there is no automated FPL buying or lineup submission.
