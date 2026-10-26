# FPL numerical review after GW7

Data collected: 2026-10-26T08:53:51.894439+00:00. Model: 0.1.1. Forecast events: 9, 10, 11, 12, 13, 14.

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

Observations: 731; model MAE: 2.1942; four-week points-average MAE: 2.5304. Lower error is better; this is not an unbiased strategy comparison.

## Rankings by position

Projected points are model estimates, not guarantees. All horizon totals are unmultiplied player points; they are not squad gains.

### Goalkeepers

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Raya | £6.2m | 4.31 | 25.59 | 77.0 |
| Tzolakis | £4.7m | 4.19 | 24.42 | 77.0 |
| Trafford | £5.0m | 3.68 | 21.88 | 77.0 |
| Verbruggen | £4.6m | 2.67 | 20.46 | 77.0 |
| Suzuki | £5.0m | 3.44 | 19.34 | 70.8 |
| Pickford | £5.5m | 2.90 | 19.02 | 77.0 |
| A.Becker | £5.5m | 3.16 | 18.71 | 77.0 |
| Donnarumma | £5.5m | 2.38 | 18.53 | 77.0 |
| Leno | £4.5m | 3.08 | 17.52 | 77.0 |
| Kelleher | £5.0m | 3.60 | 17.07 | 77.0 |
| Kinsky | £4.4m | 2.84 | 16.66 | 77.0 |
| Lammens | £4.9m | 2.07 | 16.56 | 77.0 |
| Rushworth | £4.5m | 2.79 | 14.10 | 77.0 |
| Horníček | £5.0m | 2.56 | 13.53 | 77.0 |
| Roefs | £4.9m | 2.39 | 13.04 | 77.0 |

### Defenders

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Vuskovic | £5.1m | 3.73 | 27.58 | 75.5 |
| Tarkowski | £6.2m | 4.16 | 26.42 | 77.0 |
| De Cuyper | £5.3m | 3.24 | 24.59 | 71.2 |
| Gabriel | £7.9m | 3.94 | 23.73 | 77.0 |
| Branthwaite | £5.5m | 3.61 | 23.12 | 77.0 |
| Hall | £5.3m | 4.11 | 22.96 | 76.9 |
| Bogle | £4.7m | 3.78 | 22.70 | 67.5 |
| Muharemović | £5.1m | 3.76 | 22.48 | 77.0 |
| Van Hecke | £4.9m | 4.01 | 22.34 | 77.0 |
| Jacquet | £5.1m | 3.60 | 21.96 | 74.0 |
| Silva | £5.0m | 3.71 | 21.65 | 77.0 |
| Justin | £4.5m | 3.60 | 21.52 | 75.1 |
| Egan | £4.1m | 3.77 | 21.30 | 75.3 |
| Konsa | £4.7m | 3.56 | 21.29 | 64.5 |
| O'Shea | £4.0m | 3.25 | 20.91 | 77.0 |

### Midfielders

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Mbeumo | £7.9m | 4.15 | 25.57 | 77.0 |
| Iwobi | £5.4m | 4.06 | 24.47 | 71.4 |
| Tavernier | £6.3m | 3.94 | 24.39 | 68.9 |
| Stach | £6.0m | 3.86 | 23.41 | 76.7 |
| Groß | £6.2m | 3.50 | 23.27 | 73.4 |
| Cunha | £7.9m | 3.67 | 22.56 | 58.2 |
| Tonali | £5.3m | 4.08 | 22.41 | 74.8 |
| Tielemans | £5.7m | 3.62 | 22.27 | 66.5 |
| Dewsbury-Hall | £6.6m | 3.74 | 22.24 | 77.0 |
| Rice | £7.4m | 3.57 | 21.85 | 73.8 |
| Buendía | £5.9m | 3.52 | 21.25 | 64.4 |
| Ødegaard | £6.8m | 3.38 | 20.98 | 69.9 |
| E.Le Fée | £5.7m | 3.60 | 20.97 | 74.6 |
| Gomez | £5.0m | 3.12 | 20.48 | 74.8 |
| Rogers | £8.0m | 3.42 | 20.48 | 74.9 |

### Forwards

| Player | Price | Next GW | Horizon | Expected minutes/match |
|---|---:|---:|---:|---:|
| Haaland | £15.7m | 4.92 | 30.30 | 75.3 |
| Calvert-Lewin | £6.1m | 4.14 | 25.28 | 73.8 |
| Isak | £9.0m | 3.76 | 24.74 | 57.1 |
| Evanilson | £6.2m | 3.82 | 23.92 | 72.9 |
| Barry | £5.6m | 3.94 | 22.84 | 73.7 |
| Gonzalo | £6.0m | 3.42 | 20.85 | 72.3 |
| Emersonn | £5.5m | 3.15 | 20.53 | 59.5 |
| Kostoulas | £5.8m | 3.18 | 20.38 | 60.6 |
| N.Jackson | £6.7m | 3.21 | 19.75 | 63.3 |
| Havertz | £7.5m | 2.90 | 18.19 | 66.9 |
| Marmoush | £7.0m | 3.23 | 17.36 | 57.8 |
| Wissa | £6.1m | 2.65 | 16.28 | 74.3 |
| João Pedro | £7.9m | 2.72 | 16.22 | 46.7 |
| Solanke | £5.8m | 3.00 | 15.56 | 52.0 |
| Thomas-Asante | £5.0m | 2.76 | 15.53 | 53.7 |

## Sources

- https://fantasy.premierleague.com/api/bootstrap-static/
- https://fantasy.premierleague.com/api/fixtures/
- https://fantasy.premierleague.com/api/element-summary/{player_id}/

Run `python -m fpl_planner review --force` to refresh before a deadline. Scheduling is best-effort; there is no automated FPL buying or lineup submission.
