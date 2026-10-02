# Demonstration Script (5–10 minutes)

Follow this structured workflow to demonstrate the full end-to-end scholarship intelligence lifecycle:

### Step 1: Verification of Acceptance Gates
Run the automated dataset validator:
```bash
python scripts/verify_dataset.py
```
Demonstrate that all 6 rubric requirements pass:
- **55 authentic scholarship records** (Requirement: 20+)
- **17 primary-source verified records** against official `.gov.in` sources (Requirement: 15+)
- **17 records with confidence score = 100.0% ≥ 95%** (Requirement: 10+)
- **3 distinct source types** (Scholarship Portal / Govt, University, Corporate CSR)
- **2 recorded change events** with source-backed evidence (Requirement: 2+)
- **2 expired/stale examples** (1 EXPIRED, 1 NO_LONGER_VERIFIABLE)

### Step 2: End-to-End Crawl & Change-Detection Walkthrough
Run the demonstration script:
```bash
python scripts/demonstrate_crawl_change.py
```
This demonstrates the complete assignment lifecycle:
1. **Discovery & Fetch**: Bounded crawl obeying robots.txt, capturing HTML & official scheme guideline PDFs.
2. **Extraction**: Deterministic extraction of structured fields (amount, eligibility, deadline, provider, application URL, income criteria, selection process).
3. **Official Verification**: Positively classifies trusted domains and prevents aggregator spoofing.
4. **Deterministic Confidence**: Provenance scoring (+35 official, +20 name, +45 critical fields) with reasons. Only ≥95% receives VERIFIED status.
5. **Storage & Evidence**: Persistent SQLite storage with field-level excerpts and content hashes.
6. **Repeat Crawl & Change Detection**: Compares new observations against existing values; records immutable `ChangeEvent` entries showing old value, new value, date, source URL, and exact evidence text.

### Step 3: Interactive Dashboard Review
Launch the Streamlit UI:
```bash
streamlit run dashboard/app.py
```
Demonstrate the product capabilities:
- **Overview Metrics**: Discovered count, Verified count, Review Required, Expired/Stale, and Average Confidence.
- **Search & Filtering**: Filter by Source Type, Status, Provider, and minimum confidence threshold.
- **Scholarship Detail Card**: Expand a verified record (e.g. AICTE Swanath or Pragati) to inspect official URL, application portal link, eligibility rules, amount, and deadline.
- **Evidence Drawer**: Click into verified fields to view exact source text excerpts, retrieval timestamp, and content hash.
- **Change History**: Open the Change History tab to view recorded portal updates showing Old vs. New values and official announcement excerpts.

### Step 4: FastAPI & REST Endpoints
Start the API server:
```bash
uvicorn app.main:app --reload
```
Open interactive docs at `http://localhost:8000/docs`:
- `GET /stats`: Real-time dataset metrics matching the rubric.
- `GET /scholarships`: Filtered, searchable, paginated scholarship records.
- `GET /scholarships/{id}/history`: Append-only audit trail of changes.
- `GET /scholarships/{id}/evidence`: Cryptographically traceable source snippets.

### Step 5: Automated Test Suite
Run the unit test suite:
```bash
pytest -v
```
All 14 tests pass, validating URL normalization, source classification, deterministic scoring, anti-hallucination guarantees, expired date logic, and change tracking.
