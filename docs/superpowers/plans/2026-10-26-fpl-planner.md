# FPL Planner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans inline. Steps use checkbox (`- [x]`) syntax.

**Goal:** Ship a free public GitHub repository that schedules FPL numerical reviews and keeps private squad data encrypted.
**Architecture:** Public FPL ingestion, auditable statistical forecasts, six-week MILP transfer planning, public rankings and encrypted personalised reports. GitHub handles scheduling and persistence.
**Tech Stack:** Python 3.12, unittest, scipy/HiGHS, cryptography/AES-GCM, GitHub Actions standard Ubuntu runner.
**Spec:** ../specs/2026-10-26-fpl-planner-design.md

## Global Constraints
- No Streetbot, AWS, paid APIs, large runners, workflow artifacts or caches.
- No private squad input or plaintext report in tracked files or public logs.
- Integer money in tenths; six-week horizon maximum; two transfers per week maximum; no chips in v1.
- Completed, data_checked events only; price changes and auto-subs are explicit model limitations.

## Review Focus
- Data changed during an unfinished gameweek: no leakage into forecasts.
- State advances beyond its effective gameweek: fail personalised analysis closed.
- An original player is sold and rebought: no repeated initial selling-price discount.
- Collection/network/solver failure: no success marker or partial publication.
- Secrets or personalised text appear in logs, commits or summaries: block publication.

### Task 1: collection, state and privacy
Files: src/fpl_planner/{__init__,data,state,privacy}.py, tests/test_data_state.py, requirements.txt, .gitignore, pyproject.toml.
Interfaces: FPLClient.get(path)->dict/list; collect(client,bootstrap)->snapshot; validate_state(state,players,next_gw)->dict; seal(report,key)->bytes; unseal(cipher,key)->dict.
- [x] Write and run failing tests for completed events, bounded request failures, duplicate event fixtures, state validity/staleness and authenticated encryption.
- [x] Implement validated schemas, retrying public client and compact snapshots; invalid state errors never echo input.
- [x] Run task suite, inspect output, commit.

### Task 2: deterministic forecast
Files: src/fpl_planner/forecast.py, config/model.json, tests/test_forecast.py.
Interfaces: project(snapshot,config)->list[player dict with forecasts per event and component breakdown].
- [x] Write and run failing tests for weighted rates/shrinkage, DNP versus short appearances, absent histories, confirmed unavailable players, blanks/doubles and completion cutoffs.
- [x] Implement smoothed position priors, fixture-adjusted scoring components and explicit limitations.
- [x] Run task suite, inspect output, commit.

### Task 3: transfer optimiser
Files: src/fpl_planner/optimise.py, tests/test_optimise.py.
Interfaces: solve(players,state,events,config,hold_now=False)->plan with weeks, objective, bound, gap and status; compare()->best,hold,gain.
- [x] Write and run failing tests on a small generic league for money, formation, captain, hits, rollover cap, sale/rebuy and hold baseline.
- [x] Implement scipy MILP constraints, original-ownership accounting, stable ordering and bounded solve reporting; no invented optimality claim.
- [x] Run task suite, inspect output, commit.

### Task 4: reporting and automation
Files: src/fpl_planner/{report,cli,__main__}.py, .github/workflows/{review,ci}.yml, scripts/sync_state.py, tests/test_pipeline.py, README.md.
Interfaces: run_review(root,client,state=None,key=None,force=False)->public status; decrypt CLI only writes ignored local files by default.
- [x] Write and run failing pipeline tests for skip/re-run, stale secret, partial failure, missing secrets and public output privacy.
- [x] Implement atomic public report publication and encrypted personal results, with no live private data in stdout or job summaries.
- [x] Add free scheduled workflow, read-only CI and documentation; no extra notification credentials.
- [x] Run complete tests and public live smoke; commit.

### Task 5: review and publish
- [x] Fresh reviewer checks the complete implementation against spec; fix important issues with regression tests.
- [x] Create public repository, seed Actions secrets via stdin, scan tracked files and push.
- [x] Trigger and inspect CI and one real review run; confirm a duplicate run skips.
- [x] Document limits, local key recovery and state refresh; provide repo and workflow links.
