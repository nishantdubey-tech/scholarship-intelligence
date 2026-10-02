"""Persistent normalized opportunity, evidence, and crawl history models."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Text, Float, DateTime, ForeignKey, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base

def now_utc(): return datetime.now(timezone.utc)

class Scholarship(Base):
    __tablename__ = "scholarships"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(500), index=True)
    provider: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    official_source_url: Mapped[str] = mapped_column(Text)
    application_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_type: Mapped[str] = mapped_column(String(40), default="OTHER")
    amount: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    benefit_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    eligibility: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    education_level: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    current_status: Mapped[str] = mapped_column(String(40), default="REVIEW_REQUIRED")
    confidence_score: Mapped[float] = mapped_column(Float, default=0)
    confidence_status: Mapped[str] = mapped_column(String(40), default="REVIEW_REQUIRED")
    closing_date: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc, onupdate=now_utc)
    field_data: Mapped[dict] = mapped_column(JSON, default=dict)
    verification_reasons: Mapped[list] = mapped_column(JSON, default=list)
    content_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    evidence: Mapped[list["Evidence"]] = relationship(back_populates="scholarship", cascade="all, delete-orphan")
    history: Mapped[list["ChangeEvent"]] = relationship(back_populates="scholarship", cascade="all, delete-orphan")

class Evidence(Base):
    __tablename__ = "evidence"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scholarship_id: Mapped[int] = mapped_column(ForeignKey("scholarships.id"))
    field_name: Mapped[str] = mapped_column(String(100))
    value: Mapped[str] = mapped_column(Text)
    source_url: Mapped[str] = mapped_column(Text)
    evidence_text: Mapped[str] = mapped_column(Text)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    content_hash: Mapped[str] = mapped_column(String(64))
    scholarship: Mapped[Scholarship] = relationship(back_populates="evidence")

class ChangeEvent(Base):
    __tablename__ = "change_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scholarship_id: Mapped[int] = mapped_column(ForeignKey("scholarships.id"))
    field_name: Mapped[str] = mapped_column(String(100))
    old_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    new_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    source_url: Mapped[str] = mapped_column(Text)
    evidence: Mapped[str] = mapped_column(Text)
    scholarship: Mapped[Scholarship] = relationship(back_populates="history")

class CrawlRun(Base):
    __tablename__ = "crawl_runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    pages_seen: Mapped[int] = mapped_column(Integer, default=0)
    candidates: Mapped[int] = mapped_column(Integer, default=0)
    records_updated: Mapped[int] = mapped_column(Integer, default=0)
    errors: Mapped[list] = mapped_column(JSON, default=list)

class SourceSnapshot(Base):
    __tablename__ = "source_snapshots"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_url: Mapped[str] = mapped_column(Text)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    content_hash: Mapped[str] = mapped_column(String(64), index=True)
    content_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    body_text: Mapped[str] = mapped_column(Text)
