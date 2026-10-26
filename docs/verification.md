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

## GitHub verification

- Public visibility and `main` default branch verified through GitHub API; scheduled workflow state is `active`.
- [Offline checks](https://github.com/joellimrl/fpl-planner/actions/runs/40295617209): passed on the standard Ubuntu runner.
- [Forced live review](https://github.com/joellimrl/fpl-planner/actions/runs/40295625527): passed, 669 public players, personal output encrypted, bot commit succeeded. Downloaded ciphertext decrypted with the locally retained key.
- [Duplicate check](https://github.com/joellimrl/fpl-planner/actions/runs/40295782542): passed, returned `unchanged` without recollection or re-optimisation.
- Initial hosted run exposed deprecated action runtimes. Replaced starter actions with current official checkout v7.0.1 and setup-python v7.1.0, pinned to their verified commit SHAs; subsequent CI/manual dispatch verifies these exact versions.

## Important limits

No claim of an unbiased historical strategy backtest. Starting forecast parameters are uncalibrated. The retrospective diagnostic uses current metadata and is labelled accordingly. No automatic substitutions, vice fallback, chip choices or future price changes in the MILP objective; maximum two transfers per week. Bounds/status distinguish proven-to-tolerance and limited search results. Report-only; no FPL write credentials or account actions in the scheduled system.

The scheduled workflow now reconstructs the latest published deadline squad automatically; no weekly private-state upload is required. Unpublished upcoming-deadline changes are excluded by design. Loss of the local encryption key prevents reading existing private reports. Public sync inconsistencies fail the run atomically, retaining prior dated reports. Scheduled execution is best-effort and may be disabled after 60 inactive days; no paid fallback is configured.

## Public baseline update (v0.2.0)

- Offline suite: 41 tests passed, including public reconstruction, transfer chips, price rebuy, hit reconciliation, missing history, public-over-private precedence, encrypted provenance and atomic failure.
- Real entry public sync: 15 players from published GW8, £1.7m bank and two free transfers for GW9. All 13 holdings shared with the previously saved authenticated seed had matching reconstructed purchase prices.
- The workflow no longer reads `FPL_TEAM_STATE`. Only the report encryption key remains necessary; squad data is fetched without FPL credentials.
- Fresh independent review found three important issues: arbitrary simultaneous-transfer bank ordering, a deadline passing during collection, and public validation failure replacing previous personal output. All three were reproduced RED and fixed GREEN; the full suite passed 41 tests. No new findings were deferred.
- [Hosted offline checks](https://github.com/joellimrl/fpl-planner/actions/runs/40318114141): passed.
- [Public-baseline live review](https://github.com/joellimrl/fpl-planner/actions/runs/40318115188): passed; 669 players; six forecast events GW9–14; encrypted personal report committed. Downloaded ciphertext decrypted locally and verified as published GW8, bank17, FT2. Best solve reached configured optimality tolerance with gap zero.
- [Duplicate run](https://github.com/joellimrl/fpl-planner/actions/runs/40318300221): passed, returned `unchanged` without full collection or optimisation.
- Removed obsolete repository secret `FPL_TEAM_STATE`; only `REPORT_ENCRYPTION_KEY` remains. Confirmed public repository, main default branch and active scheduled workflow.
- Implementation choice: retained this task's dedicated checkout on a feature branch, then fast-forwarded main after tests/review. No additional worktree was needed.
