"""FastAPI application for browsing scholarship records and crawl operations."""
from __future__ import annotations
from typing import Optional
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
import hmac
import os
from fastapi import FastAPI, HTTPException, Query, Header
from sqlalchemy import or_, func
from app.database.db import initialize, SessionLocal
from app.models.scholarship import Scholarship, CrawlRun, SourceSnapshot
from app.services.crawler import run_crawl

@asynccontextmanager
async def lifespan(_app):
    initialize()
    yield

app = FastAPI(title="Scholarship Intelligence", version="1.0.0", lifespan=lifespan)

@app.get("/health")
def health(): return {"status": "ok"}

@app.get("/scholarships")
def scholarships(q: Optional[str] = None, status: Optional[str] = None, source_type: Optional[str] = None,
                 provider: Optional[str] = None, education_level: Optional[str] = None,
                 category: Optional[str] = None, gender: Optional[str] = None,
                 domicile: Optional[str] = None, confidence_status: Optional[str] = None,
                 min_confidence: float = Query(0, ge=0, le=100), max_confidence: float = Query(100, ge=0, le=100),
                 page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100)):
    if min_confidence > max_confidence:
        raise HTTPException(422, "min_confidence must be less than or equal to max_confidence")
    with SessionLocal() as s:
        query = s.query(Scholarship)
        if q: query = query.filter(or_(Scholarship.name.ilike(f"%{q}%"), Scholarship.provider.ilike(f"%{q}%")))
        if status: query = query.filter(Scholarship.current_status == status.upper())
        if source_type: query = query.filter(Scholarship.source_type == source_type.upper())
        if provider: query = query.filter(Scholarship.provider.ilike(f"%{provider}%"))
        if confidence_status: query = query.filter(Scholarship.confidence_status == confidence_status.upper())
        query = query.filter(Scholarship.confidence_score >= min_confidence,
                             Scholarship.confidence_score <= max_confidence)
        rows = query.order_by(Scholarship.name).all()
        def contains(value, selected):
            if value is None: return False
            if isinstance(value, list): return any(contains(x, selected) for x in value)
            return selected.casefold() in str(value).casefold()
        if education_level: rows = [x for x in rows if contains((x.field_data or {}).get("education_level"), education_level)]
        if category: rows = [x for x in rows if contains((x.field_data or {}).get("category_criteria"), category)]
        if gender: rows = [x for x in rows if contains((x.field_data or {}).get("gender_criteria"), gender)]
        if domicile: rows = [x for x in rows if contains((x.field_data or {}).get("domicile_requirements"), domicile)]
        total = len(rows)
        rows = rows[(page-1)*page_size:page*page_size]
        return {"total": total, "page": page, "page_size": page_size, "items": [serialize(x) for x in rows]}

def serialize(x):
    return {"id": x.id, "name": x.name, "provider": x.provider, "official_source_url": x.official_source_url,
            "application_url": x.application_url, "source_type": x.source_type, "amount": x.amount,
            "eligibility": x.eligibility, "closing_date": x.closing_date, "current_status": x.current_status,
            "confidence_score": x.confidence_score, "confidence_status": x.confidence_status,
            "last_verified_at": x.last_verified_at, "created_at": x.created_at, "updated_at": x.updated_at,
            "field_data": x.field_data, "verification_reasons": x.verification_reasons}

@app.get("/scholarships/{record_id}")
def scholarship(record_id: int):
    with SessionLocal() as s:
        x=s.get(Scholarship,record_id)
        if not x: raise HTTPException(404,"Scholarship not found")
        return serialize(x)

@app.get("/scholarships/{record_id}/evidence")
def evidence(record_id: int):
    with SessionLocal() as s:
        x=s.get(Scholarship,record_id)
        if not x: raise HTTPException(404,"Scholarship not found")
        return [{"field":e.field_name,"value":e.value,"source_url":e.source_url,"evidence_text":e.evidence_text,
                 "retrieved_at":e.retrieved_at,"content_hash":e.content_hash} for e in x.evidence]

@app.get("/scholarships/{record_id}/history")
def history(record_id: int):
    with SessionLocal() as s:
        x=s.get(Scholarship,record_id)
        if not x: raise HTTPException(404,"Scholarship not found")
        return [{"field":h.field_name,"old_value":h.old_value,"new_value":h.new_value,"detected_at":h.detected_at,
                 "source_url":h.source_url,"evidence":h.evidence,"is_demonstration":h.is_demonstration,
                 "scenario_id":h.scenario_id} for h in x.history]

@app.get("/scholarships/{record_id}/snapshots")
def snapshots(record_id: int):
    with SessionLocal() as s:
        x=s.get(Scholarship,record_id)
        if not x: raise HTTPException(404,"Scholarship not found")
        urls={e.source_url for e in x.evidence}
        return [{"source_url":snapshot.source_url,"retrieved_at":snapshot.retrieved_at,
                 "content_hash":snapshot.content_hash,"content_type":snapshot.content_type,
                 "body_text":snapshot.body_text}
                for snapshot in s.query(SourceSnapshot).filter(SourceSnapshot.source_url.in_(urls)).order_by(SourceSnapshot.retrieved_at.desc()).all()]

@app.get("/stats")
def stats():
    with SessionLocal() as s:
        total=s.query(Scholarship).count()
        recent_cutoff = datetime.now(timezone.utc) - timedelta(days=30)
        recent = 0
        for row in s.query(Scholarship.updated_at).all():
            value=row[0]
            if value:
                if value.tzinfo is None: value=value.replace(tzinfo=timezone.utc)
                recent += value >= recent_cutoff
        return {"total_discovered":total,"verified":s.query(Scholarship).filter_by(confidence_status="VERIFIED").count(),
                "review_required":s.query(Scholarship).filter_by(confidence_status="REVIEW_REQUIRED").count(),
                "active":s.query(Scholarship).filter_by(current_status="ACTIVE").count(),
                "expiring_soon":s.query(Scholarship).filter_by(current_status="EXPIRING_SOON").count(),
                "expired":s.query(Scholarship).filter_by(current_status="EXPIRED").count(),
                "no_longer_verifiable":s.query(Scholarship).filter_by(current_status="NO_LONGER_VERIFIABLE").count(),
                "recently_updated_30d":recent,
                "average_confidence":s.query(func.avg(Scholarship.confidence_score)).scalar() or 0}

@app.post("/crawl")
def crawl(authorization: Optional[str] = Header(default=None)):
    expected = os.getenv("CRAWL_API_TOKEN")
    if expected and not hmac.compare_digest(authorization or "", f"Bearer {expected}"):
        raise HTTPException(401, "Bearer token required")
    return run_crawl()

@app.get("/crawl-runs")
def crawl_runs():
    with SessionLocal() as s:
        return [{"id":r.id,"started_at":r.started_at,"finished_at":r.finished_at,"pages_seen":r.pages_seen,
                 "candidates":r.candidates,"records_updated":r.records_updated,"errors":r.errors}
                for r in s.query(CrawlRun).order_by(CrawlRun.id.desc()).limit(50)]
