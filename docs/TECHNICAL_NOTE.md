# Technical note: Scholarship Intelligence

## Architecture

The local system uses Python, HTTPX, BeautifulSoup, FastAPI, SQLAlchemy and SQLite. Seed domains are bounded; discovery follows relevant same-origin links, checks `robots.txt`, deduplicates normalized URLs and limits pages per seed. The crawler isolates fetch errors per candidate so one unavailable host does not abort a run.

```text
Official seed domains → bounded discovery → candidate links → HTTP fetch
        → visible text/links → deterministic extraction → evidence checks
        → confidence + status → SQLite records, evidence and append-only history
```

## Discovery and extraction

The seed registry contains government and national scholarship/education domains. Discovery is domain-aware and keyword-guided; it does not treat third-party aggregators as sources of record. Extraction is deterministic: HTML title/headings, application-labelled links, rupee amounts and human-readable dates are retained only when found in page text. A missing value remains null. The parser stores source excerpts with each supported extracted value. Broader eligibility and criteria extraction remains a limitation and should not be represented as complete.

## Verification and confidence

Source classification uses explicit trusted domain signals (government domains, selected education bodies and scholarship portals). Confidence is deterministic: 35 points for official source, 20 for evidence-backed name, and 45 distributed equally over evidence-backed critical fields (provider, amount, eligibility, deadline, application URL). A non-official domain cannot be marked VERIFIED. Only scores ≥95 can become VERIFIED; lower scores remain REVIEW_REQUIRED. This rubric rewards provenance and completeness rather than an LLM-generated confidence value.

## Hallucination safeguards

Facts must originate in fetched page content. Missing values remain null, evidence excerpts/hash/source URLs are persisted, and each score includes reasons. The current simple extractor favors precision over coverage. It can miss content rendered only by JavaScript and complex deadline formats. Reviewers should inspect field evidence before relying on records.

## Updates and stale detection

Repeat crawls compare extracted fields with stored values. Differences create append-only change events with old/new values, time, URL and evidence excerpt. The two live crawls in the included database observed no source-field changes. Status refresh marks past parsed deadlines EXPIRED, deadlines within 30 days EXPIRING_SOON and records not verified within 45 days NO_LONGER_VERIFIABLE. It also retains an explicit NO_LONGER_VERIFIABLE status for the dated Tata Capital report that lacks a current application cycle. Missing or ambiguous dates are not guessed. A missing page alone is not yet proof of removal; this requires additional consecutive-run tracking.
