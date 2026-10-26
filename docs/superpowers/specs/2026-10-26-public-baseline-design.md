# Public deadline squad baseline

The user selected automatic public synchronisation and explicitly accepts that unpublished transfers are excluded. Replace the workflow's private squad export with public entry 5622563, retaining encrypted personal reports and the existing free public GitHub runner.

## Approach

Public picks/history/transfers are authoritative. The alternative, authenticated live exports, requires recurring user intervention and includes changes outside the requested baseline. Keep that legacy mode for local use only. Store the public entry ID in `config/entry.json`; no FPL login or squad secret is required.

Read the most recent published deadline (including an unfinished current round), independently of the latest finalised statistics round. Rebuild permanent ownership from GW1 picks, season-start prices (`now_cost - cost_change_start`) and chronological public transaction purchase costs. Reconcile the reconstructed squad and bank against published picks/history. Free Hit transactions and its temporary picks/bank must not replace permanent ownership. Wildcard transactions persist. Derive available transfers from consecutive history rows, checking hits; normal weeks add one up to five, Wildcard/Free Hit retain their previous allowance without adding one. Reject missing history, unsupported late joining, unknown chips/rule overrides or inconsistent transactions rather than guessing finances.

## Reporting and execution

Use the published bank and recompute sale prices at current market prices. The baseline is effective for the next event. Include source deadline, permanent squad deadline, bank, available transfers and the explicit unpublished-change limitation inside the encrypted personal report. No entry-specific data enters the league-wide snapshot/report. Public read failures abort atomically and retain the previous successful report with its date; do not fall back to an old private state. Cache markers include the published deadline and resolved-state fingerprint, so completed GW and deadline changes both refresh safely.

## Verification

Synthetic tests cover original holdings, transfer/rebuy costs, free-transfer rolls/cap/hits/chips, Free Hit restoration, incomplete history, mismatches, unpublished future transaction exclusion and pipeline precedence/privacy/cache/failure atomicity. Run the full offline suite, then public API synchronisation and a live Actions run. Confirm encrypted personal output and duplicate skip. No new dependencies or paid services.
