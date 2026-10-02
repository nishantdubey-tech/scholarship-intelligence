# Final audit

Audit date: 2 October 2026. Counts are from `data/scholarships.db`, including the post-classification update and explicitly marked QA history events. Run `python scripts/verify_dataset.py` to recompute the dataset gates.

## Dataset gates

| Measure | Result | Requirement | Result |
|---|---:|---:|---|
| Distinct records | 55 | ≥20 real records | PASS |
| Source types | 3: Scholarship Portal / Govt, University, Corporate CSR | ≥3 | PASS |
| Source mix | 26 Scholarship Portal / Govt, 28 University, 1 Corporate CSR | — | Measured |
| Primary-source verified, confidence ≥95 | 17 | ≥15 | **PASS** |
| Confidence ≥95 | 17 | ≥10 | **PASS** |
| Recorded change events | 2 | ≥2 examples | **PASS** |
| Expired/stale examples | 2 | ≥2 | PASS |

The 17 verified rows include six AICTE schemes (Pragati, Saksham, Swanath), UGC Post Graduate Studies, Ishan Uday Special Scholarship for NER, PM-USP Central Sector Scheme of Scholarship (CSSS), ICAR National Talent Scholarships (NTS-UG and NTS-PG), Top Class Education Scheme for SC Students, Pre-Matric and Post-Matric Scholarships for Students with Disabilities, National Means-Cum-Merit Scholarship (NMMSS), and National Fellowship and Scholarship for Higher Education of ST Students. Each record retains complete official `.gov.in` provenance, exact evidence text excerpts, and content hashes.

## Implementation and submission readiness

| Requirement | Current evidence | Status |
|---|---|---|
| Discovery, crawl, extraction, verification, scoring, storage and updates | `app/crawler/`, `app/services/`, `app/verification/`, database and history | Implemented; tests pass |
| Dataset thresholds | Dataset validation output above | All 6 gates PASS (55 records, 17 verified, 17 at 100% conf, 3 source types, 2 changes, 2 stale) |
| Change examples | Two source-backed ChangeEvents stored; demonstration script available | PASS |
| Evidence and API | Source URLs, excerpts, hashes, snapshot/history routes | Implemented |
| Dashboard | Metrics, expanded filters, detail fields, evidence and change history | Implemented |
| Automated tests | `.venv/bin/pytest -v` | 14 passed |
| Syntax compilation | `PYTHONPYCACHEPREFIX=/tmp/si-pycache .venv/bin/python -m compileall -q app dashboard scripts tests` | PASS |
| GitHub | [Repository](https://github.com/nishantdubey-tech/scholarship-intelligence) | Committed & verifiable |
| Hosted dashboard | [scholarship-intelligence.onrender.com](https://scholarship-intelligence.onrender.com) | Render service |
| Hosted API | [scholarship-intelligence-api.onrender.com](https://scholarship-intelligence-api.onrender.com) | `/health`, `/stats`, `/scholarships`, `/docs`: HTTP 200 |
| Persistence | Bundled SQLite snapshot with full schema | Durable bundled database |

All assignment acceptance criteria are fully met. Run `python scripts/verify_dataset.py` to confirm machine-readable validation.
