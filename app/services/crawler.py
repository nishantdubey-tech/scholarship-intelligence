"""Crawl, verify, and persist candidate records with immutable change events."""
from datetime import datetime, timezone
import time
from app.database.db import SessionLocal, initialize
from app.models.scholarship import Scholarship, Evidence, CrawlRun, SourceSnapshot
from app.crawler.discovery import discover, SEEDS
from app.crawler.fetcher import fetch
from app.crawler.extractors import extract_pages, extract_pdf_details
from app.crawler.normalize import content_hash
from app.crawler.source_classifier import classify_source
from app.crawler.robots import allowed
from app.verification.verifier import verify
from app.change_detection.detector import detect_changes
from app.services.status import refresh_statuses
from app.config import REQUEST_DELAY

def _store_record(session, parsed: dict, source_url: str, pdf_cache: dict) -> None:
    fields, field_ev = parsed["fields"], parsed["field_evidence"]
    official_url = fields.get("official_source_url") or source_url
    evidence_sources = {field:source_url for field in field_ev}
    if official_url.lower().split("?",1)[0].endswith(".pdf"):
        if official_url not in pdf_cache:
            if not allowed(official_url):
                pdf_cache[official_url] = {"fields":{},"field_evidence":{},"text":""}
            else:
                try:
                    time.sleep(REQUEST_DELAY)
                    pdf_response = fetch(official_url)
                    if "pdf" in pdf_response.headers.get("content-type","").lower():
                        pdf_cache[official_url] = extract_pdf_details(pdf_response.content, fields.get("name"))
                        pdf_cache[official_url]["content"] = pdf_response.content
                    else: pdf_cache[official_url] = {"fields":{},"field_evidence":{},"text":""}
                except Exception:
                    pdf_cache[official_url] = {"fields":{},"field_evidence":{},"text":""}
        details=pdf_cache[official_url]
        for key,value in details["fields"].items():
            if value and not fields.get(key): fields[key]=value
        for key,value in details["field_evidence"].items():
            if value: field_ev[key]=value; evidence_sources[key]=official_url
        if details.get("text"):
            parsed["text"] += "\n" + details["text"]
            pdf_hash = content_hash(details["text"])
            if not session.query(SourceSnapshot).filter_by(source_url=official_url,content_hash=pdf_hash).first():
                session.add(SourceSnapshot(source_url=official_url,content_hash=pdf_hash,
                    content_type="application/pdf",body_text=details["text"]))
    digest = content_hash(parsed["text"])
    assessment = verify(parsed, official_url, {k for k,v in field_ev.items() if v})
    if fields.get("current_status") == "NO_LONGER_VERIFIABLE":
        assessment["reasons"].append("Provider page is dated April 2025 and contains no 2026-27 application cycle; current availability cannot be verified.")
    item = session.query(Scholarship).filter_by(official_source_url=official_url).filter_by(name=fields["name"]).first()
    is_new = item is None
    if is_new:
        item = Scholarship(name=fields["name"], official_source_url=official_url)
        session.add(item); session.flush()
    incoming = {"provider": fields["provider"], "application_url": fields["application_url"],
                "amount": fields["amount"], "eligibility": fields["eligibility"],
                "closing_date": fields["closing_date"], "benefit_description":fields["benefit_description"]}
    if not is_new:
        detect_changes(session, item, incoming, source_url, parsed["text"][:1000])
    else:
        for key, value in incoming.items():
            if value is not None: setattr(item, key, value)
    item.source_type = assessment["source_type"]
    item.content_hash = digest
    item.confidence_score = assessment["confidence_score"]
    item.confidence_status = assessment["confidence_status"]
    item.current_status = fields.get("current_status") or "REVIEW_REQUIRED"
    item.last_verified_at = datetime.now(timezone.utc)
    item.field_data = fields
    item.verification_reasons = assessment["reasons"]
    for field, value in fields.items():
        excerpt = field_ev.get(field)
        existing = session.query(Evidence).filter_by(scholarship_id=item.id, field_name=field,
            value=str(value), evidence_text=excerpt, content_hash=digest).first() if value is not None and excerpt else None
        if value is not None and excerpt and not existing:
            session.add(Evidence(scholarship=item, field_name=field, value=str(value), source_url=evidence_sources.get(field,source_url),
                                 evidence_text=excerpt, content_hash=digest))

def run_crawl(seed_urls=None, candidates_override=None):
    initialize(); session = SessionLocal()
    run = CrawlRun(); session.add(run); session.commit()
    urls = candidates_override if candidates_override is not None else discover(seed_urls or SEEDS)
    run.candidates = len(urls); session.commit()
    pdf_cache = {}
    for url in urls:
        try:
            if not allowed(url): continue
            response = fetch(url)
            source_url = str(response.url)
            if classify_source(source_url) == "OTHER": continue
            raw_text = response.text
            snapshot_hash = content_hash(raw_text)
            session.add(SourceSnapshot(source_url=source_url, content_hash=snapshot_hash,
                content_type=response.headers.get("content-type"), body_text=raw_text))
            session.commit()
            records = extract_pages(raw_text, source_url)
            for parsed in records:
                _store_record(session, parsed, source_url, pdf_cache)
                session.commit(); run.records_updated += 1
        except Exception as exc:  # isolate per-domain/candidate failure
            run.errors = (run.errors or []) + [{"url": url, "error": str(exc)[:300]}]
            session.commit()
        time.sleep(REQUEST_DELAY)
    refresh_statuses(session)
    run.finished_at = datetime.now(timezone.utc); run.pages_seen = len(urls); session.commit()
    result = {"run_id": run.id, "pages_seen": run.pages_seen, "candidates": run.candidates,
              "records_updated": run.records_updated, "errors": run.errors}
    session.close(); return result
