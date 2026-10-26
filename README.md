# FPL Planner

A numerical Fantasy Premier League research pipeline. A public GitHub repository owns the code, public statistical snapshots, scheduling and reports. No Streetbot, AWS account, OpenAI key or FPL password is needed.

## Cost contract

- Only **standard `ubuntu-latest` GitHub-hosted runners in a public repository**. Workflows skip if the repo becomes private. GitHub currently provides these runs free: [billing documentation](https://docs.github.com/en/actions/concepts/billing-and-usage).
- No paid APIs, AI calls, AWS resources, custom domains, larger runners, artifacts, dependency caches, container registry, Pages hosting or outbound notification provider.
- Packages are downloaded from public PyPI. Public FPL GET endpoints need no API token. Their availability and schemas are not guaranteed.
- Host policies can change. This is a zero-paid-service design, not a promise that third-party free services run forever. If the required free runner becomes unavailable, stop; do not substitute a paid service.

## What runs

Hourly at minute 23 UTC, `FPL gameweek review` fetches FPL metadata. It runs full collection only for a newly completed **and data-checked** gameweek, changed private state, or a manual forced refresh. Initial setup processes the latest completed gameweek, rather than generating every old report. Forecasts start at the next deadline (`is_next`), not an unfinished current round.

New public reports appear in [reports/latest.md](reports/latest.md). Compact, gzip-compressed evidence is kept under `data/snapshots` and component forecasts under `data/forecasts`. One workflow writer commits the outputs together. Repeated unchanged checks skip collection and optimisation. Scheduled runs may be delayed; use manual dispatch before a deadline when needed. GitHub may disable scheduled public workflows after 60 days without repository activity; re-enable after the off-season. We do not make artificial keepalive commits.

### Privacy

This is a **public repository**. Public reports contain league-wide rankings, source links, assumptions and forecast diagnostics, never the private live squad, bank or personalised transfers. Your FPL identifier is not needed in public config.

`FPL_TEAM_STATE` is a repository Actions secret. It contains a minimal squad export: effective gameweek, bank, available free transfers, player IDs and purchase/selling prices. No password, cookie or session token is used. State is valid for its explicit gameweek only; after that public research continues and personal analysis reports `state_refresh_required` until you upload a new export. Changes outside the planner require another refresh. Sale prices are recalculated from current price and stored purchase price.

Personalised results are AES-256-GCM encrypted **before** being saved in `reports/private/*.enc`. `REPORT_ENCRYPTION_KEY` is a generated Actions secret and an ignored local `.private/report.key` file. The public manifest uses keyed HMAC fingerprints, not a brute-forceable plain hash of your finances. Private plaintext is never written to workflow summaries, log output or tracked files. Tests use generic synthetic squads. PR checks are read-only and receive no secrets.

**Back up `.private/report.key` securely.** GitHub cannot show a saved Actions secret back to you. Without the key, existing reports cannot be decrypted. Keep local `.private` files out of cloud/public sharing. Rotating a key protects future reports; it does not recover old ones.

## Local use

Python 3.12 or newer; pinned package versions match the tested Python 3.12 workflow.

```sh
python -m venv .venv
# Activate the environment for your operating system.
python -m pip install --no-cache-dir -r requirements.txt
python -m pip install --no-deps -e .
python -m unittest discover -s tests -v
python -m fpl_planner review
```

Manual cloud refresh, using your existing GitHub CLI login:

```sh
gh workflow run review.yml --repo joellimrl/fpl-planner -f force=true
gh run list --repo joellimrl/fpl-planner
```

Fetch and read the private report locally:

```sh
git pull --ff-only
python -m fpl_planner decrypt
```

This writes readable Markdown to ignored `.private/latest-report.md`, using `.private/report.key`. The key never goes in a command-line argument. An already-existing local key is preserved on setup.

To refresh exact squad finances, save the authenticated FPL `my-team` JSON export locally in `.private` (do not include cookies/headers), then:

```sh
python scripts/sync_state.py --repo joellimrl/fpl-planner --input .private/my-team.json --gameweek 10
gh workflow run review.yml --repo joellimrl/fpl-planner -f force=true
```

The upload tool passes data to `gh secret set` through stdin, never shell arguments or stdout. A direct state JSON has this shape (integer prices are tenths of a million):

```json
{
  "effective_gameweek": 10,
  "bank": 5,
  "free_transfers": 1,
  "squad": [
    {"element": 123, "purchase_price": 50, "selling_price": 51}
  ]
}
```

Supply all 15 unique picks with valid positional counts and at most three per club. `FPL_TEAM_STATE` and `REPORT_ENCRYPTION_KEY` are the only manual secrets; GitHub provides its own short-lived `GITHUB_TOKEN` with scoped repository-content write permission. Optional notifications are deliberately excluded from v1.

## Numerical model

See [config/model.json](config/model.json). v1 uses complete gameweeks only; exponential recency decay 0.85 per gameweek; 450 pseudo-minutes shrinking xG/xA rates to position priors; smoothed historical playing-time, bonus, cards and defensive threshold frequencies. Opponent strength is based on smoothed completed-match goals and conceded goals, with a bounded venue adjustment. Fixtures in a double are summed; blank gameweeks score zero.

Each forecast exposes appearance, goal, assist, clean-sheet, defensive contribution, bonus, save and deduction components. Goal weights are GK 10 / DEF 6 / MID 5 / FWD 4; assists 3. These scoring rules are described by [FPL](https://www.premierleague.com/en/news/2174909/). Availability flags are applied conservatively through the entire horizon, not assumed to mean a guaranteed return next week.

**These parameters are starting assumptions, not fitted or proven predictive weights.** The public retrospective MAE check compares historical-row forecasts with a four-week points-average baseline. It is explicitly not an unbiased decision backtest: current club/position metadata, current data revisions and missing historical injuries/prices prevent that claim. Archived as-of snapshots enable stronger evaluation over time.

## Optimisation contract

SciPy/HiGHS MILP chooses squad, transfers, starting XI and captain across up to six gameweeks. It enforces 2 GK/5 DEF/5 MID/3 FWD, at most three per club, a legal 11-player formation, integer-tenths budgets and actual initial sale prices. Original-ownership variables prevent selling and rebuying from reusing the initial selling-price discount. Prices are held constant after the snapshot.

Up to **two transfers per gameweek**, with extra transfers charged four points after using free transfers. Free transfers roll up to five. Compare the best first action against holding now while still allowing transfers later in **both** plans. Model objective is expected starter points plus extra captain points minus hits. Bench points are never simply added. No chip optimisation, automatic-substitution expectation or vice-captain fallback in v1; bench and vice suggestions are ranked by forecasts. Saved transfers beyond the final horizon have no fitted terminal value.

Same snapshot/config and solver version define the mathematical problem. HiGHS is deterministic under fixed conditions, but operational wall-clock limits can yield different feasible incumbents across hardware. Each report exposes status, node count, bound and relative gap. A limit-reached plan is not a proven optimum. The difference between two incumbents is not a certified gain if the bound interval crosses zero. The system does not automatically submit transfers or lineups to FPL.

## Sources and design

- [FPL players and gameweek metadata](https://fantasy.premierleague.com/api/bootstrap-static/)
- [FPL fixtures](https://fantasy.premierleague.com/api/fixtures/)
- Player histories: `https://fantasy.premierleague.com/api/element-summary/{id}/`
- [Design](docs/superpowers/specs/2026-10-26-fpl-planner-design.md)
- [Implementation plan](docs/superpowers/plans/2026-10-26-fpl-planner.md)

Unofficial personal research project. No affiliation with Fantasy Premier League.
