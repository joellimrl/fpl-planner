# FPL numerical review after GW11

Data collected: 2026-11-24T23:33:21.532836+00:00. Model: 0.2.0. Forecast events: 12, 13, 14, 15, 16, 17.

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
| Tzolakis | £4.7m | 4.68 | 27.54 | 79.0 |
| Trafford | £5.1m | 4.60 | 25.75 | 79.0 |
| Verbruggen | £4.7m | 4.09 | 24.52 | 79.0 |
| Roefs | £4.8m | 4.09 | 23.27 | 79.0 |
| A.Becker | £5.5m | 3.55 | 21.63 | 79.0 |
| Kinsky | £4.4m | 3.71 | 20.00 | 79.0 |
| Pickford | £5.5m | 2.95 | 18.71 | 79.0 |
| Kelleher | £5.0m | 3.08 | 18.61 | 79.0 |
| Leno | £4.5m | 3.03 | 17.90 | 79.0 |
| Lammens | £4.8m | 2.48 | 16.58 | 79.0 |
| Suzuki | £5.1m | 2.51 | 16.25 | 76.3 |
| Sels | £5.0m | 2.37 | 15.46 | 79.0 |
| Donnarumma | £5.4m | 2.38 | 15.42 | 79.0 |
| Horníček | £5.0m | 1.84 | 15.25 | 79.0 |
| Petrović | £4.5m | 2.71 | 15.17 | 79.0 |

### Defenders

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Hill | £5.6m | 4.86 | 28.18 | 79.0 |
| Gabriel | £8.1m | 4.36 | 27.66 | 79.0 |
| Muharemović | £5.1m | 4.91 | 26.99 | 79.0 |
| Konsa | £4.9m | 4.27 | 26.95 | 73.5 |
| Van Hecke | £5.2m | 4.92 | 26.63 | 79.0 |
| Vuskovic | £5.3m | 4.35 | 25.59 | 78.4 |
| De Cuyper | £5.5m | 4.41 | 25.50 | 73.2 |
| Justin | £4.5m | 4.69 | 25.45 | 77.4 |
| Silva | £5.1m | 4.27 | 24.66 | 79.0 |
| Jacquet | £5.1m | 4.00 | 24.45 | 77.7 |
| Virgil | £6.4m | 3.96 | 24.24 | 79.0 |
| Araujo | £5.5m | 3.83 | 23.44 | 66.6 |
| Branthwaite | £5.5m | 3.49 | 22.03 | 69.3 |
| Bogle | £4.8m | 4.09 | 21.52 | 74.1 |
| Elvedi | £4.5m | 3.92 | 21.26 | 66.3 |

### Midfielders

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Tavernier | £6.8m | 4.40 | 26.57 | 75.1 |
| Groß | £6.3m | 4.49 | 25.38 | 77.4 |
| E.Le Fée | £5.7m | 4.00 | 25.12 | 76.5 |
| Wirtz | £7.4m | 4.09 | 25.12 | 71.8 |
| Ødegaard | £6.7m | 3.93 | 24.13 | 75.5 |
| Rice | £7.5m | 3.84 | 23.51 | 73.0 |
| McAtee | £5.5m | 4.01 | 22.50 | 70.8 |
| Gomez | £5.1m | 3.94 | 22.41 | 75.6 |
| Rudoni | £5.0m | 3.22 | 22.35 | 71.7 |
| Ayari | £5.5m | 3.78 | 21.53 | 67.2 |
| Lewis-Potter | £5.5m | 3.77 | 21.42 | 66.1 |
| Dewsbury-Hall | £6.7m | 3.42 | 21.27 | 75.2 |
| Rogers | £8.3m | 3.26 | 20.65 | 78.1 |
| Kamara | £5.0m | 3.40 | 20.46 | 77.3 |
| Rayan | £6.3m | 3.37 | 20.33 | 77.0 |

### Forwards

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Evanilson | £6.6m | 4.50 | 27.43 | 74.4 |
| Haaland | £15.8m | 3.90 | 27.41 | 78.3 |
| N.Jackson | £7.3m | 4.60 | 27.23 | 68.7 |
| Barry | £5.7m | 4.24 | 26.48 | 73.0 |
| Isak | £9.3m | 4.30 | 26.43 | 68.0 |
| McBurnie | £5.5m | 4.71 | 24.51 | 78.1 |
| Calvert-Lewin | £6.0m | 4.63 | 24.35 | 77.1 |
| Havertz | £7.4m | 3.31 | 20.15 | 63.8 |
| Delap | £5.3m | 3.55 | 18.97 | 68.6 |
| Kostoulas | £5.7m | 3.27 | 18.41 | 58.3 |
| Gonzalo | £5.8m | 2.90 | 15.97 | 59.9 |
| Solanke | £5.8m | 2.81 | 15.89 | 49.5 |
| Strand Larsen | £5.9m | 2.47 | 15.67 | 47.8 |
| Emersonn | £5.4m | 2.69 | 14.97 | 50.7 |
| Marmoush | £7.0m | 2.59 | 14.86 | 53.4 |

## Sources

- https://fantasy.premierleague.com/api/bootstrap-static/
- https://fantasy.premierleague.com/api/fixtures/
- https://fantasy.premierleague.com/api/element-summary/{player_id}/

Run `python -m fpl_planner review --force` to refresh before a deadline. Scheduling is best-effort; there is no automated FPL buying or lineup submission.
