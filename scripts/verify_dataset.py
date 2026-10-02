#!/usr/bin/env python3
"""Audit actual stored data against minimum submission thresholds."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.database.db import SessionLocal, initialize
from app.models.scholarship import Scholarship, ChangeEvent

initialize()
with SessionLocal() as s:
    rows=s.query(Scholarship).all()
    verified=[x for x in rows if x.confidence_status=="VERIFIED" and x.official_source_url and x.last_verified_at and x.evidence]
    high=[x for x in verified if x.confidence_score>=95]
    grounded=[x for x in rows if x.official_source_url and x.evidence]
    types={x.source_type for x in grounded}
    changes=s.query(ChangeEvent).count()
    stale=sum(x.current_status in {"EXPIRED","NO_LONGER_VERIFIABLE"} for x in rows)
    checks=[("20+ real records",len(rows)>=20),("15+ primary-source verified",len(verified)>=15),
            ("10+ confidence >=95%",len(high)>=10),("3+ source types",len(types)>=3),
            ("2+ recorded changes",changes>=2),("2+ expired/stale",stale>=2)]
    print("# Dataset Validation\n")
    print(f"Total scholarships: {len(rows)}\nOfficially verified: {len(verified)}\nConfidence >=95%: {len(high)}")
    print(f"Source types across evidence-backed records: {len(types)}\nChange examples: {changes}\nExpired/stale examples: {stale}\n")
    for label,ok in checks: print(f"{'PASS' if ok else 'FAIL'} {label}")
    if not all(ok for _,ok in checks): sys.exit(1)
    print("\nPASS")
