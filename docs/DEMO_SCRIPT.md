# Demonstration script (5–10 minutes)

1. Show the architecture and safeguards in the README: official sources, bounded crawl, evidence excerpts, deterministic confidence and nulls for unsupported facts.
2. Start with `streamlit run dashboard/app.py`. Show the dataset KPIs and filter by status, source, provider, confidence and deadline. Open a record and inspect official/application links, available eligibility fields, field evidence, retrieval date/hash and score reasons.
3. Run `uvicorn app.main:app --reload`, then open `/docs`. Show `/stats`, `/scholarships`, one record's `/evidence`, `/snapshots` and `/history` routes.
4. Demonstrate the QA history behavior by running `python scripts/simulate_change.py`. It adds two `DEMONSTRATION ONLY` events on an existing record and does not change any scholarship facts. Show the labelled entries in dashboard/API history. Never call these observed or source-backed changes.
5. Run `python scripts/verify_dataset.py`. Report the validator's exact result. At this audit the repository has 55 records, 9 primary-source verified, 9 at 95%+, three source types and two stale/expired examples. The verified and high-confidence numeric gates remain short, and there are zero live source changes.
6. If time permits, run `python scripts/crawl.py` to show bounded discovery, fetches, extraction attempts, per-page errors and persistence. A changed history row only counts as genuine when a later crawl captured supporting source evidence.

The project does not claim every numeric acceptance gate passes. Keep the audit report beside the live demo so these limitations are visible to the evaluator.
