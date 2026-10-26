# Verification record

## Independent review

A fresh reviewer checked source, tests and workflows through f57de63. They found two important issues: the next planning deadline was absent from the cache identity, and a rejected/missing private state left obsolete `latest.enc` output accessible. Both were reproduced with failing tests and fixed in 644b570. The suite then passed 28 tests.

The reviewer found the transfer-minimum, five-free-transfer cap, original-player sale/rebuy accounting, budgets and formation constraints consistent. One minor observation was retained as a known boundary: solver output is independently checked for bounds/integrality, while linear-row feasibility relies on HiGHS rather than a second full matrix evaluator. The comment now describes the actual check. Regression tests exercise the financial and formation constraints on synthetic leagues.

## Local checks

- Python 3.12 virtual environment with pinned requirements.
- `PYTHONPATH=src python -m unittest discover -s tests -v`: 28 passed.
- Live public FPL collection: 669 players; latest complete/data-checked event was GW7, with forecasts starting at next deadline GW9 while GW8 was unfinished.
- Full six-week private optimisation: feasible, reached configured optimality tolerance with reported gap zero. This verifies the solver integration, not the predictive accuracy of the forecast.
- Personal state/key ignored by git; personalised report encrypted and locally decryptable.
- Workflow YAML parsed locally; the real GitHub standard-runner execution is verified during publication.

## Important limits

No claim of an unbiased historical strategy backtest. Starting forecast parameters are uncalibrated. The retrospective diagnostic uses current metadata and is labelled accordingly. No automatic substitutions, vice fallback, chip choices or future price changes in the MILP objective; maximum two transfers per week. Bounds/status distinguish proven-to-tolerance and limited search results. Report-only; no FPL write credentials or account actions in the scheduled system.

Private state must be refreshed for every new planning gameweek and after changes made outside the planner. Loss of the local encryption key prevents reading existing private reports. Public research continues when private state is unavailable. Scheduled execution is best-effort and may be disabled after 60 inactive days; no paid fallback is configured.
