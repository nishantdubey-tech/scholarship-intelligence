# Demonstration script (5–10 minutes)

1. `pip install -r requirements.txt`; copy `.env.example` to `.env` and set a contactable crawler user agent.
2. `python scripts/seed_sources.py` to show legitimate seed domains.
3. `python scripts/crawl.py` to demonstrate bounded discovery, extraction attempts, per-page errors and saved records. Do not claim a record was found unless output/database confirms it.
4. `uvicorn app.main:app --reload`; open `/docs`, `/stats`, `/scholarships`, and a record's evidence/history endpoints.
5. `streamlit run dashboard/app.py`; search the live dataset and inspect source links, evidence excerpts, score reasons and history.
6. Run `python scripts/crawl.py` again. Compare crawl runs and append-only change history.
7. Run `python scripts/verify_dataset.py`. It exits non-zero until all numeric assignment thresholds are met; show the result honestly.

The local QA mutation script is explicitly marked as synthetic and must not be presented as scholarship data or as a genuine source change. A genuine change demonstration requires two source snapshots with a real changed value.
