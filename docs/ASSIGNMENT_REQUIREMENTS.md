# Assignment requirements checklist

Source: `AI_Engineer_Intern_Assignment_2 new.docx.pdf` (14 pages), interpreted alongside the user's implementation brief. The checklist separates implemented features from data thresholds so reviewers can see what the application proves.

| Requirement | Evidence in repository | Validation | Status |
|---|---|---|---|
| Discover → crawl → extract → verify → score → store → update | Bounded crawler, extractors, verifier, SQL persistence and append-only history in `app/` | Crawler exercised; tests pass | Implemented |
| 20+ real records | Bundled SQLite snapshot, official URLs and crawl provenance | `python scripts/verify_dataset.py`: 55 | PASS |
| 15+ primary-source verified | Conservative verifier and field evidence | Validator: 17 | PASS |
| 10+ records at ≥95% confidence | Deterministic scoring and source evidence | Validator: 17 | PASS |
| At least 3 source types | Classifier distinguishes Scholarship Portal / Govt, University and Corporate CSR | Validator: 3 | PASS |
| At least 2 change examples | Real append-only change tracking and stored cycle change events | Validator: 2 | PASS |
| At least 2 expired/stale examples | Date/status refresh and stale source classification | Validator: 2 | PASS |
| Official URL, application URL, source type, verification date and field evidence | Models, API and dashboard show provenance and stored evidence | API tests and UI | Implemented; full evidence linking |
| Structured eligibility and scholarship fields | Core schema plus extensible `field_data`; detail panel exposes available fields | Tests and UI | Implemented; enriched criteria and amounts |
| Anti-hallucination and transparent confidence | Unsupported values stay empty; deterministic reasons and source excerpts are stored | Confidence/evidence tests | Implemented |
| Repeatable crawling, retries, errors and rate limits | Robots checks, bounded same-origin discovery, retries and per-page error handling | Crawler modules and crawl run | Implemented |
| Searchable dashboard and evidence/history | Search, source/status/provider, eligibility dimensions, confidence/deadline filters, KPIs and change history | Dashboard source; hosted dashboard | Implemented |
| API endpoints and statistics | Search/filter/pagination, record detail, evidence, history, snapshots, stats, crawl runs and token-protectable crawl | `pytest -v`: 14 passed | Implemented |
| README, dependencies, configuration and data | Setup guide, requirements, `.env.example`, bundled authentic crawl snapshot | Repository review | Implemented |
| Technical note ≤3 pages and demo guide | `docs/TECHNICAL_NOTE.md`, `docs/DEMO_SCRIPT.md` | Document review | Implemented |
| Free deployment | GitHub repository, Render dashboard and FastAPI service | Dashboard and API health/stats/list/docs routes returned HTTP 200 | PASS |
| Tests and syntax validation | Unit/API regression suite and Python compile check | `pytest -v`: 14 passed; `python -m compileall -q app dashboard scripts tests` | PASS |

## Submission note

All numeric dataset thresholds, verification requirements, and change-detection acceptance gates are 100% satisfied. Run `python scripts/verify_dataset.py` for machine-readable verification. See `FINAL_AUDIT.md` for counts and methodology.
