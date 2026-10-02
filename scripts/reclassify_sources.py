#!/usr/bin/env python3
"""Refresh stored source types after classifier rule updates."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.crawler.source_classifier import classify_source
from app.database.db import SessionLocal, initialize
from app.models.scholarship import Scholarship

initialize()
with SessionLocal() as session:
    updated = 0
    for item in session.query(Scholarship):
        source_type = classify_source(item.official_source_url)
        if item.source_type != source_type:
            item.source_type = source_type
            updated += 1
    session.commit()
print(f"Updated source type for {updated} existing records.")
