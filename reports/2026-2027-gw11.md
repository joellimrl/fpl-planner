# FPL numerical review after GW11

Data collected: 2026-11-27T23:38:27.522684+00:00. Model: 0.2.0. Forecast events: 13, 14, 15, 16, 17, 18.

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

Observations: 911; model MAE: 1.976; four-week points-average MAE: 2.1567. Lower error is better; this is not an unbiased strategy comparison.

## Rankings by position

Projected points are model estimates, not guarantees. All horizon totals are unmultiplied player points; they are not squad gains.

### Goalkeepers

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Tzolakis | £4.7m | 5.19 | 27.65 | 79.0 |
| Trafford | £5.1m | 3.73 | 25.49 | 79.0 |
| Verbruggen | £4.7m | 3.61 | 24.48 | 79.0 |
| Roefs | £4.8m | 3.34 | 22.82 | 79.0 |
| A.Becker | £5.5m | 4.15 | 21.47 | 79.0 |
| Kinsky | £4.5m | 3.69 | 19.00 | 79.0 |
| Kelleher | £5.0m | 3.13 | 18.69 | 79.0 |
| Pickford | £5.5m | 2.96 | 18.46 | 79.0 |
| Leno | £4.5m | 3.20 | 17.97 | 79.0 |
| Lammens | £4.8m | 2.55 | 17.57 | 79.0 |
| Raya | £6.2m | 2.46 | 16.83 | 56.9 |
| Horníček | £5.0m | 2.90 | 16.76 | 79.0 |
| Suzuki | £5.1m | 3.02 | 16.32 | 76.3 |
| Donnarumma | £5.4m | 2.89 | 15.81 | 79.0 |
| Sels | £5.0m | 2.58 | 15.51 | 79.0 |

### Defenders

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Hill | £5.7m | 4.11 | 28.34 | 79.0 |
| Gabriel | £8.1m | 4.05 | 28.02 | 79.0 |
| Konsa | £4.9m | 4.02 | 27.32 | 73.5 |
| Muharemović | £5.2m | 3.87 | 26.52 | 79.0 |
| Van Hecke | £5.2m | 4.90 | 25.47 | 79.0 |
| Vuskovic | £5.3m | 3.71 | 25.32 | 78.4 |
| De Cuyper | £5.6m | 3.63 | 25.04 | 73.2 |
| Justin | £4.5m | 3.59 | 24.90 | 77.4 |
| Silva | £5.1m | 3.51 | 24.88 | 79.0 |
| Jacquet | £5.1m | 4.71 | 24.34 | 77.7 |
| Virgil | £6.4m | 4.69 | 24.13 | 79.0 |
| Araujo | £5.5m | 4.50 | 23.39 | 66.6 |
| Branthwaite | £5.5m | 3.55 | 21.86 | 69.3 |
| Ajer | £4.5m | 3.46 | 21.31 | 79.0 |
| Murillo | £5.5m | 3.35 | 20.87 | 79.0 |

### Midfielders

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Tavernier | £6.8m | 4.21 | 27.49 | 75.1 |
| E.Le Fée | £5.7m | 3.61 | 25.57 | 76.5 |
| Wirtz | £7.5m | 4.62 | 25.25 | 71.8 |
| Groß | £6.3m | 3.88 | 24.69 | 77.4 |
| Ødegaard | £6.7m | 3.55 | 23.97 | 75.5 |
| Rice | £7.5m | 3.54 | 23.42 | 73.0 |
| Rudoni | £5.0m | 4.09 | 22.58 | 71.7 |
| McAtee | £5.5m | 3.48 | 22.23 | 70.8 |
| Gomez | £5.1m | 3.44 | 21.86 | 75.6 |
| Dewsbury-Hall | £6.7m | 3.57 | 21.41 | 75.2 |
| Lewis-Potter | £5.5m | 3.24 | 21.35 | 66.1 |
| Rayan | £6.3m | 3.19 | 21.07 | 77.0 |
| Barnes | £6.0m | 3.94 | 21.05 | 77.7 |
| Ayari | £5.5m | 3.30 | 20.99 | 67.2 |
| Rogers | £8.3m | 4.17 | 20.92 | 78.1 |

### Forwards

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Evanilson | £6.6m | 4.41 | 28.57 | 74.4 |
| Haaland | £15.7m | 4.34 | 28.03 | 78.3 |
| Barry | £5.7m | 4.54 | 26.85 | 73.0 |
| N.Jackson | £7.3m | 4.34 | 26.67 | 68.7 |
| Isak | £9.4m | 4.83 | 26.64 | 68.0 |
| McBurnie | £5.5m | 4.22 | 23.58 | 78.1 |
| Calvert-Lewin | £6.0m | 3.72 | 23.22 | 77.1 |
| Havertz | £7.4m | 2.97 | 19.91 | 63.8 |
| Delap | £5.3m | 2.81 | 18.60 | 68.6 |
| Kostoulas | £5.7m | 2.87 | 17.88 | 58.3 |
| Strand Larsen | £5.9m | 2.71 | 15.82 | 47.8 |
| Solanke | £5.8m | 2.80 | 15.64 | 49.5 |
| Gonzalo | £5.8m | 2.56 | 15.56 | 59.9 |
| Emersonn | £5.4m | 2.67 | 15.10 | 50.7 |
| Marmoush | £7.0m | 2.58 | 14.69 | 53.4 |

## Sources

- https://fantasy.premierleague.com/api/bootstrap-static/
- https://fantasy.premierleague.com/api/fixtures/
- https://fantasy.premierleague.com/api/element-summary/{player_id}/

Run `python -m fpl_planner review --force` to refresh before a deadline. Scheduling is best-effort; there is no automated FPL buying or lineup submission.
