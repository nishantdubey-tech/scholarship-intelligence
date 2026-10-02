# Final audit

Audit date: 2 October 2026. Counts below come from the persisted SQLite database after reprocessing saved official PDF snapshots and reviewing extracted fields for cross-scheme and outdated-cycle contamination.

## Dataset gates

| Measure | Result | Requirement | Status |
|---|---:|---:|---|
| Distinct crawled scholarship records | 55 | ≥20 real records | PASS |
| Source types represented | 3 (government, university, corporate CSR) | ≥3 | PASS |
| Source mix | 26 government, 28 university, 1 corporate CSR | — | Measured |
| VERIFIED at confidence ≥95 | 9 | ≥15 | FAIL |
| Confidence ≥95 | 9 | ≥10 | FAIL |
| Source-backed change events | 0 | ≥2 | FAIL |
| Expired/no-longer-verifiable examples | 2 | ≥2 | PASS |

The 9 VERIFIED rows consist of six current AICTE schemes, UGC Post Graduate Studies, Ishan Uday, and PM-USP CSSS. The Railway PMSS row is deliberately review-required because its linked guideline limits eligibility to 2022–23. Shared disability-scheme PDFs do not contribute a scalar amount because their rates vary by category. No scholarship records or source-backed changes were fabricated. The `simulate_change.py` helper is a QA demonstration only and is not included in the source-backed change count.

## Implementation audit

| Requirement | Status | Evidence | Test/validation |
|---|---|---|---|
| Discovery → crawl → extract → verify → score → store → update | Implemented | `app/crawler/`, `app/services/crawler.py` | Live crawl persisted 55 records |
| ≥20 real records | PASS | 55 source-linked rows in `data/scholarships.db` | `python scripts/verify_dataset.py` |
| ≥15 officially verified; ≥10 at ≥95 | FAIL | 9 meet strict confidence and evidence criteria | `python scripts/verify_dataset.py` |
| ≥3 source types | PASS | Government, university, corporate CSR | Dataset audit |
| ≥2 source-backed change examples | FAIL | No field change was observed across repeat crawls; QA simulation is labeled and excluded | Change-history table; dataset audit |
| ≥2 expired/stale examples | PASS | 1 expired CSSS listing and 1 no-current-cycle corporate source | Dataset audit |
| Source, application URL, evidence and retrieval metadata | Implemented | Evidence and snapshot tables retain excerpts, hashes and source URLs | API smoke check |
| Anti-hallucination safeguards | Implemented with limits | Unsupported values remain null; questionable PDF fields were removed | Extractor and confidence tests; manual row audit |
| Repeatable crawling, robots, rate limit and per-page failure handling | Implemented | Bounded crawler modules | Crawl run and tests |
| Searchable dashboard with evidence/history | Implemented | `dashboard/app.py` | Dashboard launched locally |
| FastAPI endpoints | Implemented | `app/main.py` | `/health`, `/stats`, `/scholarships`: HTTP 200 |
| Test suite | PASS | 11 tests passed | `.venv/bin/pytest -q` |
| Python compilation | PASS | `compileall` completed | `python -m compileall` |
| GitHub repository / hosted deployment | NOT DONE | No Git remote, hosting account, or deployment credentials available | Not applicable |

The dataset gate exits non-zero as required. It passes 20+ records, three source types and two stale/expired examples, and fails the verified-count, high-confidence-count and source-backed-change-count gates. Do not describe this project as submission-ready until those three data gates are met.
