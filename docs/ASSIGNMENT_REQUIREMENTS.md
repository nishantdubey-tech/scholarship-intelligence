# Assignment requirements checklist

Source: `AI_Engineer_Intern_Assignment_2 new.docx.pdf` (14 pages). This checklist reflects the complete assignment and its pasted implementation brief. Status is intentionally evidence-based.

| Requirement | Implementation | File/module | Test or validation | Demonstration evidence | Status |
|---|---|---|---|---|---|
| Discover → crawl → extract → verify → score → store → update | Bounded same-origin discovery, fetch, parse, source gate, score, SQL persistence and history | `app/crawler/`, `app/services/crawler.py` | `pytest`; run `python scripts/crawl.py` | CLI output and DB | Implemented; live crawl run and persisted |
| 20+ real scholarships | Live records from three official pages/source domains; no synthetic rows | `scripts/verify_dataset.py`, `data/scholarships.db` | Validation gate | Dataset audit | **PASS: 55** |
| 15+ official verifications; 10+ ≥95% | Conservative official domain signals and field-level scoring | `app/verification/` | confidence tests + dataset gate | Dataset audit | **FAIL: 9 / 9** |
| ≥3 source types | Domain classifier | `app/crawler/source_classifier.py` | source classification test | DB source_type | Implemented; PASS: 3 source types |
| ≥2 changes and ≥2 expired/stale examples | Append-only event model; time-based and source-cycle status checks | `app/change_detection/`, `app/services/status.py` | Dataset gate | History panel | **Partial: 0 source-backed changes; 2 expired/stale** |
| Official source, application URL, source type, last verified and evidence | Persisted field/source evidence | `app/models/scholarship.py` | API and extraction tests | Detail view/API | Implemented |
| Structured fields incl. eligibility, dates, conditions, requirements | Core columns plus extensible JSON field_data | `app/models/scholarship.py` | extraction tests | API detail | Partial; parser currently extracts limited fields |
| Authenticity, anti-hallucination, evidence-based 95% gate | Conservative signal rules; VERIFIED requires ≥95 and official type | `app/verification/` | confidence tests | reasons/evidence display | Partial; official organization classifier needs expansion |
| Repeatable crawler and retries/errors/rate limits/robots | bounded crawl, retries, timeout, delay, robots policy | `app/crawler/` | crawl exercise | second CLI run | Implemented; runtime exercised |
| Searchable dashboard and detail/history/evidence | Streamlit dashboard | `dashboard/app.py` | Streamlit process launched; health endpoint previously returned 200 | local dashboard | Implemented and run |
| Database and API endpoints | SQLite / SQLAlchemy; FastAPI routes | `app/database/`, `app/main.py` | `/health`, `/stats`, `/scholarships` returned HTTP 200 | `/docs` | Implemented and smoke-tested |
| README, requirements, config, sample data, setup | README and requirements; no synthetic sample rows by design | `README.md`, `.env.example` | setup commands | local demo | Partial |
| Technical note ≤3 pages and working demo guide | concise note and honest demo script | `docs/TECHNICAL_NOTE.md`, `docs/DEMO_SCRIPT.md` | review | screen demonstration | Implemented |
| Free tools only; deployment preparation | OSS dependencies, Dockerfile and Render Blueprint | `requirements.txt`, `Dockerfile`, `render.yaml` | Render build and live page verified | Public dashboard URL in README | Dashboard deployed; API local only; free filesystem ephemeral |
| PDF evaluation criteria and automatic-failure audit | final audit includes unmet gates | `docs/FINAL_AUDIT.md` | dataset validation | audit report | Audit completed; data gates remain failed |
