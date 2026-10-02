# Scholarship Intelligence

A source-grounded scholarship discovery and review system for Indian students. It crawls official sources, stores field-level evidence and deterministic confidence reasons, tracks source changes, and provides a searchable dashboard and API. Unsupported facts stay empty; demonstration history is marked and is not a genuine source change.

## Assignment Status and Dataset Validation

The system satisfies all explicit minimum-output acceptance gates specified in the Assignment 2 rubric:

| Evaluation Criterion | Minimum Target | Stored Dataset Result | Status |
| :--- | :--- | :--- | :--- |
| **Real scholarship records** | 20+ records | **55 authentic records** | **PASS** |
| **Primary/official-source verified** | 15+ records | **17 records verified against official sources** | **PASS** |
| **High confidence (≥95%)** | 10+ records | **17 records at 100.0% confidence** | **PASS** |
| **Source diversity** | 3+ source types | **3 types** (Scholarship Portal / Govt, University, Corporate CSR) | **PASS** |
| **Change-detection history** | 2+ examples | **2 recorded source-backed ChangeEvents** | **PASS** |
| **Stale / expired detection** | 2+ examples | **2 examples** (1 EXPIRED, 1 NO_LONGER_VERIFIABLE) | **PASS** |

Run `python scripts/verify_dataset.py` for machine-readable verification of all acceptance criteria.

## Architecture and stack

Python 3.11+, HTTPX, BeautifulSoup, FastAPI, SQLAlchemy, SQLite and Streamlit. The crawler performs bounded same-domain discovery, checks robots.txt, applies a request delay, extracts visible evidence and isolates page errors. FastAPI serves records, evidence, snapshots, history, statistics and crawl operations. Streamlit provides filters, confidence metrics, evidence and history review.

## Setup and run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set a contactable `CRAWLER_USER_AGENT` in `.env`. `DATABASE_URL` defaults to the bundled `data/scholarships.db`.

```bash
python scripts/seed_sources.py
python scripts/crawl.py
uvicorn app.main:app --reload
streamlit run dashboard/app.py
```

API docs are at `/docs`. Routes include `/health`, `/scholarships` (search, filters and pagination), `/scholarships/{id}`, `/evidence`, `/history`, `/snapshots`, `/stats`, `/crawl-runs` and `POST /crawl`. Set `CRAWL_API_TOKEN` to require a Bearer token for crawl requests.

## Validation and demonstration

```bash
pytest -v
python scripts/verify_dataset.py
python scripts/demonstrate_crawl_change.py
python scripts/simulate_change.py
```

`verify_dataset.py` audits all stored records and confirms all 6 rubric acceptance criteria pass. `demonstrate_crawl_change.py` runs an end-to-end walkthrough showing discovery, official verification, deterministic scoring, evidence preservation, and change detection. See [the demo guide](docs/DEMO_SCRIPT.md), [requirements checklist](docs/ASSIGNMENT_REQUIREMENTS.md), [final audit](docs/FINAL_AUDIT.md) and [technical note](docs/TECHNICAL_NOTE.md).

## Deployment

The private GitHub repository is [nishantdubey-tech/scholarship-intelligence](https://github.com/nishantdubey-tech/scholarship-intelligence). The Streamlit demo is [scholarship-intelligence.onrender.com](https://scholarship-intelligence.onrender.com); the FastAPI service is [scholarship-intelligence-api.onrender.com](https://scholarship-intelligence-api.onrender.com), with interactive docs at `/docs`. Both services were deployed from commit `52b8eb1`. The API has a generated `CRAWL_API_TOKEN` in the Blueprint. The included SQLite snapshot is bundled into each service, so their databases are separate. Render's free filesystem is ephemeral and services can sleep; crawl changes are not durable across restarts.

## Safeguards and limits

Confidence is deterministic and evidence-based. A score alone does not prove current availability; records lacking sufficient current primary-source evidence remain under review. The extractor does not render JavaScript and may miss complex eligibility/deadline rules. Removal is not inferred from one failed fetch. Respect site terms, robots policies and configured request delays.
