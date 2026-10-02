"""FastAPI application for browsing scholarship records and crawl operations."""
from __future__ import annotations
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
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
                 page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100)):
    with SessionLocal() as s:
        query = s.query(Scholarship)
        if q: query = query.filter(or_(Scholarship.name.ilike(f"%{q}%"), Scholarship.provider.ilike(f"%{q}%")))
        if status: query = query.filter(Scholarship.current_status == status.upper())
        if source_type: query = query.filter(Scholarship.source_type == source_type.upper())
        total = query.count(); rows = query.order_by(Scholarship.name).offset((page-1)*page_size).limit(page_size).all()
        return {"total": total, "page": page, "items": [serialize(x) for x in rows]}

def serialize(x):
    return {"id": x.id, "name": x.name, "provider": x.provider, "official_source_url": x.official_source_url,
            "application_url": x.application_url, "source_type": x.source_type, "amount": x.amount,
            "eligibility": x.eligibility, "closing_date": x.closing_date, "current_status": x.current_status,
            "confidence_score": x.confidence_score, "confidence_status": x.confidence_status,
            "last_verified_at": x.last_verified_at, "field_data": x.field_data, "verification_reasons": x.verification_reasons}

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
                 "source_url":h.source_url,"evidence":h.evidence} for h in x.history]

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
        return {"total_discovered":total,"verified":s.query(Scholarship).filter_by(confidence_status="VERIFIED").count(),
                "review_required":s.query(Scholarship).filter_by(confidence_status="REVIEW_REQUIRED").count(),
                "active":s.query(Scholarship).filter_by(current_status="ACTIVE").count(),
                "expired":s.query(Scholarship).filter_by(current_status="EXPIRED").count(),
                "average_confidence":s.query(func.avg(Scholarship.confidence_score)).scalar() or 0}

@app.post("/crawl")
def crawl(): return run_crawl()

@app.get("/crawl-runs")
def crawl_runs():
    with SessionLocal() as s:
        return [{"id":r.id,"started_at":r.started_at,"finished_at":r.finished_at,"pages_seen":r.pages_seen,
                 "candidates":r.candidates,"records_updated":r.records_updated,"errors":r.errors}
                for r in s.query(CrawlRun).order_by(CrawlRun.id.desc()).limit(50)]
