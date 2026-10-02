# Final audit

Audit date: 2 October 2026. Counts are from `data/scholarships.db`, including the post-classification update and explicitly marked QA history events. Run `python scripts/verify_dataset.py` to recompute the dataset gates.

## Dataset gates

| Measure | Result | Requirement | Result |
|---|---:|---:|---|
| Distinct records | 55 | ≥20 real records | PASS |
| Source types | 3: Scholarship Portal, University, Corporate CSR | ≥3 | PASS |
| Source mix | 26 Scholarship Portal, 28 University, 1 Corporate CSR | — | Measured |
| Primary-source verified, confidence ≥95 | 9 | ≥15 | **FAIL** |
| Confidence ≥95 | 9 | ≥10 | **FAIL** |
| Genuine source-backed change events | 0 | ≥2 examples | **FAIL** |
| Demonstration-only change events | 2 | Not counted as genuine | QA illustration only |
| Expired/stale examples | 2 | ≥2 | PASS |

The 9 verified rows are six current AICTE schemes, UGC Post Graduate Studies, Ishan Uday and PM-USP CSSS. Ambiguous, shared-scheme and outdated-cycle evidence remains review-required. The Railway PMSS row is not counted as verified because the linked guideline only supports a 2022–23 eligibility cycle. No award amount, deadline or scholarship record was invented to meet a numeric target.

## Implementation and submission readiness

| Requirement | Current evidence | Status |
|---|---|---|
| Discovery, crawl, extraction, verification, scoring, storage and updates | `app/crawler/`, `app/services/`, `app/verification/`, database and history | Implemented; tests pass |
| Dataset thresholds | Dataset validation output above | 20+ records, three types and two stale examples pass; verified/high-confidence thresholds fail |
| Change examples | Two marked QA events; zero source-observed events | Partial; demonstrate simulation as simulation only |
| Evidence and API | Source URLs, excerpts, hashes, snapshot/history routes | Implemented |
| Dashboard | Metrics, expanded filters, detail fields, evidence and labelled history | Implemented |
| Automated tests | `.venv/bin/pytest -q` | 14 passed |
| Syntax compilation | `PYTHONPYCACHEPREFIX=/tmp/si-pycache .venv/bin/python -m compileall -q app dashboard scripts tests` | PASS |
| GitHub | [Private repository](https://github.com/nishantdubey-tech/scholarship-intelligence) | Existing; updates pushed after review |
| Hosted dashboard | [scholarship-intelligence.onrender.com](https://scholarship-intelligence.onrender.com) | Existing Render free service |
| Hosted API | Added as second service in `render.yaml` with generated crawl token | Blueprint sync/deployment must be confirmed in Render |
| Persistence | Bundled SQLite on free service | Ephemeral; dashboard/API each hold independent snapshots |

This submission is not a pass on every assignment acceptance criterion. The validator should remain non-zero until primary-source evidence supports the missing verified records, confidence threshold, and genuine changed source fields. The two demonstration events exist to make change-history behavior reviewable; they cannot satisfy a genuine-change requirement if the evaluator requires observed changes.
