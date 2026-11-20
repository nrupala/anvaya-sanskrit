# Provenance — Anvaya Sanskrit (in proving)

This repo holds the proving work of Anvaya Sanskrit: the chain, the two hand-derived golds, and the gate record. Copied on 2026-11-20 from the house work archive — the *Sanskrit spike* record (2026-11-19) and the *Sanskrit profile* record (2026-11-19/20).

## File map

| In this repo | Source |
|---|---|
| chain/ (segmenter, adapter, runner, scorer, analyze, tests, probes, sentence sets, chain token output) | Sanskrit profile record — chain/ |
| chain/rule_reader.py | Sanskrit spike record — rule_reader.py (the preserved rule reader) |
| gold/GOLD.md, gold/gold.json | Sanskrit spike record — the fixture gold (Pañcatantra, Kathāmukha; 29 relations) |
| gold/GOLD-HELDOUT.md | Sanskrit profile record — chain/GOLD-HELDOUT.md (Pañcatantra, Mitrabheda; 38 relations) |
| GATE-RECORD.md | Sanskrit profile record — STATUS.md (the Stage 1 gate record) |
| record/VERDICT.md, record/FLAW-AUDIT.md | Sanskrit spike record |

## Components and their origins

- The rule reader, the sandhi segmenter, the adapter, the runner, and the scorer are house code, written for the spike and the gate.
- vidyut is a pinned external dependency (lipi transliteration; kosha candidate analyses). The vidyut code library is MIT-licensed. It is named here as a dependency; it is not vendored into this repo.
- **Data exclusion, plainly:** the chain reads vidyut kosha DATA at run time. That data's licence was NOT independently verified by this house, so no kosha data and no vidyut data files are included in this repo — code, golds, and records only. The data-licence check is owed before any future use of that data.

State lines, unchanged: **IN PROVING — no release, nothing for sale. Release gate: NOT RUN. Guardian Mesh: NOT RUN.**
