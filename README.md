# Scholarship Intelligence

A local-first crawler and review dashboard for authentic scholarship opportunities available to Indian students. The system is designed around source provenance: it stores official URLs, field evidence, retrieval hashes, deterministic confidence reasons and append-only change history. It does not seed invented scholarship facts.

## Current dataset status

The included SQLite database contains 55 live-crawled records: 26 government portal schemes, 28 St. Xavier's University scholarship offerings, and one Tata Capital Pankh programme record. After reprocessing official PDF snapshots and removing cross-scheme or historical-cycle values, 9 records are VERIFIED at 95% or higher. The dataset has 3 source types and 2 expired/stale examples. No fabricated scholarships or source-backed change events were inserted.

The assignment validation currently fails three data gates: 15 official verifications (9 available), 10 records at ≥95% (9 available), and 2 observed source-backed changes (0 observed). The Railway PMSS listing remains review-required because its linked guideline only supports a 2022–23 eligibility cycle. Run `python scripts/verify_dataset.py` to see the exact non-zero result. See `docs/FINAL_AUDIT.md` for the audit.

## Stack and architecture

Python 3.11+, HTTPX, BeautifulSoup, FastAPI, SQLAlchemy, SQLite and Streamlit. The crawler performs bounded same-domain discovery from a seed registry, respects robots.txt, waits between requests, normalizes URLs, extracts visible HTML evidence and isolates errors. FastAPI documents endpoints at `/docs`; Streamlit displays searchable records, evidence and history.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set `CRAWLER_USER_AGENT` in `.env` to identify your use and provide contact details. `DATABASE_URL` defaults to `data/scholarships.db`. Database tables are initialized automatically by the API/crawler.

## Run

```bash
python scripts/seed_sources.py
python scripts/crawl.py
uvicorn app.main:app --reload
streamlit run dashboard/app.py
pytest
python scripts/verify_dataset.py
```

The API includes `GET /health`, `GET /scholarships` (query, status/source filters and pagination), `GET /scholarships/{id}`, evidence, history and snapshot routes, `GET /stats`, `POST /crawl`, and `GET /crawl-runs`.

## Discovery, extraction and verification

Seeds are a starting point, not a list of scholarship records. The crawler follows relevant same-origin links up to configured limits, then extracts page headings, labeled application links, dates and amounts using deterministic rules. Unsupported values remain null. Source classification recognizes selected government and education domains; uncertain sources remain review-required. Confidence awards points only for official provenance and evidence-backed fields. VERIFIED requires both an official source classification and a score of at least 95.

Each evidence row records field name/value, source URL, excerpt, retrieval timestamp and content hash. Each crawl also stores a raw page snapshot and hash. On repeat crawls, field changes append history events with old/new values and source evidence. The two live crawls in the included DB found no factual field changes, so change history is empty. Deadline/status refresh derives expired and expiring-soon states from parseable dates; stale verification becomes NO_LONGER_VERIFIABLE after 45 days. Source removal needs further consecutive-miss logic and is not inferred from a single failed request.

## Dashboard and deployment

Run locally with Streamlit as above. API container: `docker build -t scholarship-intelligence . && docker run -p 8000:8000 scholarship-intelligence`. SQLite data persistence requires mounting a volume and setting `DATABASE_URL`.

### Render hosted demo

`render.yaml` defines a free Streamlit web service. After the repository is pushed, connect the private GitHub repository to Render and create a Blueprint from `render.yaml`. The dashboard uses the included SQLite snapshot. Free Render services have an ephemeral filesystem and can sleep after inactivity, so crawl updates do not persist across restarts; use a paid persistent disk or a managed database for durable operation. The service has not been deployed yet, so no live URL is available.

## Limitations and responsible crawling

The current extractor is deliberately conservative and does not render JavaScript. Source classification is domain-signal based and should be manually reviewed; it cannot prove organizational ownership in all cases. It does not yet track repeated missing-page evidence. Respect robots policies, the configured request delay, site terms and reasonable load. No paid APIs, scraping services, secrets or aggregator-derived facts are used.
