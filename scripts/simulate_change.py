#!/usr/bin/env python3
"""Create a local change event only for an existing crawled scholarship (for demo QA)."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.database.db import SessionLocal, initialize
from app.models.scholarship import Scholarship
from app.change_detection.detector import detect_changes
initialize()
with SessionLocal() as s:
    item=s.query(Scholarship).first()
    if not item: raise SystemExit("No real crawled record available; run the crawler first.")
    detect_changes(s,item,{"benefit_description":"CHANGE TEST — restore from next source crawl"},item.official_source_url,
                   "Local demonstration mutation; not source evidence and must not be submitted as scholarship fact.")
    s.commit()
    print(f"Recorded QA-only change for record {item.id}; this mutation is not verified source data.")
