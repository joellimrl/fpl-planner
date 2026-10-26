# Public Baseline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Automatically rebuild the latest published FPL squad without private exports.

**Architecture:** A public state resolver reconstructs ownership and finances, then the existing encrypted report pipeline validates and optimises it. Public config selects this mode over legacy private state.

**Tech Stack:** Existing Python 3.12, unittest, urllib and GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-10-26-public-baseline-design.md`

## Global Constraints

- No new dependencies or paid services.
- No FPL credentials or weekly manual export in scheduled mode.
- Personal results remain encrypted; only public entry ID is configured.
- Unsupported/inconsistent finances fail without replacing prior successful output.

## Review Focus

Same-time transfers and sell/rebuy ownership; public API rollover during collection; temporary Free Hit ownership and finances; season/late-entry boundaries; secrets and stale baseline dates in published files. Add tests to the owning task for these cases.

### Task 1: Resolve public baseline

**Files:** `src/fpl_planner/public_state.py`, `tests/test_public_state.py`.

**Interfaces:** `load_public_state(client, bootstrap, entry_id, next_gw) -> dict` returns the existing state schema plus `baseline` metadata; raises ValueError for unsafe reconstruction.

- [x] Write synthetic tests for purchase reconstruction, roll/cap/hits, both transfer chips, Free Hit restoration, future rows, missing data, late entry and rollover mismatch.
- [x] Run `python -m unittest tests.test_public_state -v`; expect RED because resolver is absent.
- [x] Implement resolver; validate bank and squad, whitelist chip/rule support, exclude unpublished changes.
- [x] Run `python -m unittest discover -s tests -v`; expect PASS; commit resolver and tests.

### Task 2: Integrate and deploy

**Files:** `report.py`, `cli.py`, workflow, `config/entry.json`, README, pipeline tests.

**Interfaces:** `run_review(..., entry_id=None)` resolves public state when configured, before cache fingerprinting. CLI reads public config; workflow removes FPL_TEAM_STATE.

- [x] Write tests for public precedence, cache change/skip, encrypted provenance and failure atomicity; run to see RED.
- [x] Wire public resolver; add encrypted provenance and human-readable baseline notice; update docs and workflow.
- [x] Run full unittest suite; expect PASS. Resolve the real public squad and reconcile prices against existing seed without logging private payloads.
- [x] Review complete diff, fix important findings with RED/GREEN tests, merge verified branch and push. Run Actions; expect successful encrypted report, then duplicate skip.
- [x] Record test and cloud verification evidence.

