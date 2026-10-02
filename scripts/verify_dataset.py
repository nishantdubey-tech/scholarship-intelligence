#!/usr/bin/env python3
"""Audit stored source records and clearly separated change demonstrations."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.database.db import SessionLocal, initialize
from app.models.scholarship import Scholarship, ChangeEvent

initialize()
with SessionLocal() as session:
    rows = session.query(Scholarship).all()
    verified = [x for x in rows if x.confidence_status == "VERIFIED" and x.confidence_score >= 95
                and x.official_source_url and x.last_verified_at and x.evidence]
    high = [x for x in rows if x.confidence_score >= 95]
    grounded = [x for x in rows if x.official_source_url and x.evidence]
    types = {x.source_type for x in grounded}
    live_events = session.query(ChangeEvent).filter_by(is_demonstration=False).all()
    demo_events = session.query(ChangeEvent).filter_by(is_demonstration=True).all()
    # Count only complete examples, and count simulated events as examples only
    # when their evidence and scenario metadata make the distinction explicit.
    valid_live = [e for e in live_events if e.old_value and e.new_value and e.source_url and e.evidence]
    valid_demo = [e for e in demo_events if e.old_value and e.new_value and e.source_url and e.evidence
                  and e.scenario_id and "DEMONSTRATION ONLY" in e.evidence]
    changes = len(valid_live) + len(valid_demo)
    stale = sum(x.current_status in {"EXPIRED", "NO_LONGER_VERIFIABLE"} for x in rows)
    checks = [
        ("20+ real records", len(rows) >= 20),
        ("15+ primary-source verified", len(verified) >= 15),
        ("10+ confidence >=95%", len(high) >= 10),
        ("3+ source types", len(types) >= 3),
        ("2+ change examples (live or explicitly simulated)", changes >= 2),
        ("2+ expired/stale examples", stale >= 2),
    ]
    print("# Dataset Validation\n")
    print(f"Total scholarships: {len(rows)}")
    print(f"Officially verified (>=95%): {len(verified)}")
    print(f"Confidence >=95%: {len(high)}")
    print(f"Source types across evidence-backed records: {len(types)}")
    print(f"Change examples: {changes} ({len(valid_live)} live, {len(valid_demo)} demonstration-only)")
    print(f"Expired/stale examples: {stale}\n")
    for label, passed in checks:
        print(f"{'PASS' if passed else 'FAIL'} {label}")
    if not all(passed for _, passed in checks):
        sys.exit(1)
    print("\nPASS")
