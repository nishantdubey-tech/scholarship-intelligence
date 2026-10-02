# Assignment requirements checklist

Source: `AI_Engineer_Intern_Assignment_2 new.docx.pdf` (14 pages), interpreted alongside the user's implementation brief. The checklist separates implemented features from data thresholds so reviewers can see what the application proves.

| Requirement | Evidence in repository | Validation | Status |
|---|---|---|---|
| Discover → crawl → extract → verify → score → store → update | Bounded crawler, extractors, verifier, SQL persistence and append-only history in `app/` | Crawler exercised; tests pass | Implemented |
| 20+ real records | Bundled SQLite snapshot, official URLs and crawl provenance | `python scripts/verify_dataset.py`: 55 | PASS |
| 15+ primary-source verified | Conservative verifier and field evidence | Validator: 9 | **FAIL: 6 short** |
| 10+ records at ≥95% confidence | Deterministic scoring and source evidence | Validator: 9 | **FAIL: 1 short** |
| At least 3 source types | Classifier distinguishes Scholarship Portal, University and Corporate CSR | Validator: 3 | PASS |
| At least 2 change examples | Real append-only change tracking plus clearly marked QA scenario | 0 live; 2 demonstration-only | **Partial: no source-observed changes** |
| At least 2 expired/stale examples | Date/status refresh and stale source classification | Validator: 2 | PASS |
| Official URL, application URL, source type, verification date and field evidence | Models, API and dashboard show provenance and stored evidence | API tests and UI | Implemented; per-record completeness varies |
| Structured eligibility and scholarship fields | Core schema plus extensible `field_data`; detail panel exposes available fields | Tests and UI | Implemented; extraction coverage is incomplete |
| Anti-hallucination and transparent confidence | Unsupported values stay empty; deterministic reasons and source excerpts are stored | Confidence/evidence tests | Implemented with coverage limits |
| Repeatable crawling, retries, errors and rate limits | Robots checks, bounded same-origin discovery, retries and per-page error handling | Crawler modules and crawl run | Implemented |
| Searchable dashboard and evidence/history | Search, source/status/provider, eligibility dimensions, confidence/deadline filters, KPIs and labelled history | Dashboard source; hosted dashboard | Implemented |
| API endpoints and statistics | Search/filter/pagination, record detail, evidence, history, snapshots, stats, crawl runs and token-protectable crawl | `pytest -q`: 14 passed | Implemented |
| README, dependencies, configuration and data | Setup guide, requirements, `.env.example`, bundled authentic crawl snapshot | Repository review | Implemented |
| Technical note ≤3 pages and demo guide | `docs/TECHNICAL_NOTE.md`, `docs/DEMO_SCRIPT.md` | Document review | Implemented |
| Free deployment | GitHub private repository and hosted Render dashboard; Blueprint also defines API | Hosted dashboard previously verified; API Blueprint needs sync/verification | Dashboard deployed; API deployment pending sync |
| Tests and syntax validation | Unit/API regression suite and Python compile check | `pytest -q`: 14 passed; `PYTHONPYCACHEPREFIX=/tmp/si-pycache .venv/bin/python -m compileall -q app dashboard scripts tests` | PASS |

## Submission note

The numeric dataset validator intentionally returns a failing exit code for the 15 verified and 10 high-confidence thresholds. Genuine source changes have not been observed in the saved repeat crawls. The two stored history entries are expressly demonstration-only and must not be presented as source evidence. See `FINAL_AUDIT.md` for counts and interpretation.
