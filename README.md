# Scholarship Intelligence

A source-grounded scholarship discovery and review system for Indian students. It crawls official sources, stores field-level evidence and deterministic confidence reasons, tracks source changes, and provides a searchable dashboard and API. Unsupported facts stay empty; demonstration history is marked and is not a genuine source change.

## Assignment status

The included SQLite snapshot contains 55 records from three source types: 26 Scholarship Portal, 28 University and 1 Corporate CSR. The strict audit currently finds 9 records at 95%+ confidence, 9 primary-source verified records, 2 expired/stale examples, and 0 genuine source-backed changes. Two explicitly labelled QA history events demonstrate the change-history UI without changing scholarship facts. Run `python scripts/verify_dataset.py` for the machine-readable acceptance gates. The 15 verified and 10 high-confidence targets remain unmet; do not present the project as passing those gates.

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
pytest -q
python scripts/verify_dataset.py
python scripts/simulate_change.py
```

The validator exits non-zero while numeric data gates fail. The simulator creates two `DEMONSTRATION ONLY` history entries against a real record and does not alter scholarship fields. It must not be described as a genuine source change. See [the demo guide](docs/DEMO_SCRIPT.md), [requirements checklist](docs/ASSIGNMENT_REQUIREMENTS.md), [final audit](docs/FINAL_AUDIT.md) and [technical note](docs/TECHNICAL_NOTE.md).

## Deployment

The private GitHub repository is [nishantdubey-tech/scholarship-intelligence](https://github.com/nishantdubey-tech/scholarship-intelligence). The Streamlit demo is [scholarship-intelligence.onrender.com](https://scholarship-intelligence.onrender.com). `render.yaml` defines both the dashboard and a FastAPI service; if the Blueprint has not yet synchronized after a code update, sync it in Render to create the API service. The API has a generated `CRAWL_API_TOKEN` in the Blueprint. The included SQLite snapshot is bundled into each service, so their databases are separate. Render's free filesystem is ephemeral and services can sleep; crawl changes are not durable across restarts.

## Safeguards and limits

Confidence is deterministic and evidence-based. A score alone does not prove current availability; records lacking sufficient current primary-source evidence remain under review. The extractor does not render JavaScript and may miss complex eligibility/deadline rules. Removal is not inferred from one failed fetch. Respect site terms, robots policies and configured request delays.
