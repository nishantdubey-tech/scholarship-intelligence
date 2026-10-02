#!/usr/bin/env python3
"""Re-extract official PDF fields from stored page snapshots without refetching."""
import sys
import re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.database.db import SessionLocal, initialize
from app.models.scholarship import Scholarship, SourceSnapshot, Evidence
from app.crawler.extractors import extract_pdf_details
from app.verification.verifier import verify

initialize()
with SessionLocal() as session:
    changed=0
    for item in session.query(Scholarship).all():
        snapshot=session.query(SourceSnapshot).filter_by(
            source_url=item.official_source_url,content_type="application/pdf"
        ).order_by(SourceSnapshot.id.desc()).first()
        if not snapshot: continue
        details=extract_pdf_details(snapshot.body_text,item.name)
        fields=dict(item.field_data or {})
        # The Railway PDF currently linked by NSP explicitly limits eligibility
        # to 2022-23. Keep that historical source in snapshots, but do not treat
        # it as current eligibility evidence for the 2026-27 portal listing.
        if item.id == 26 and re.search(r"20\s*22-23",details["fields"].get("eligibility", ""),re.I):
            details["fields"].pop("eligibility",None)
            details["field_evidence"].pop("eligibility",None)
            fields["current_status"]="REVIEW_REQUIRED"
            item.current_status="REVIEW_REQUIRED"
        updated=False
        pdf_fields={"amount","eligibility","benefit_description","selection_process","renewal_requirements"}
        session.query(Evidence).filter(Evidence.scholarship_id==item.id,
            Evidence.source_url==item.official_source_url,Evidence.field_name.in_(pdf_fields)).delete(synchronize_session=False)
        for field in pdf_fields:
            value=details["fields"].get(field)
            if field in {"amount","eligibility"}:
                fields[field]=value
                setattr(item,field,value)
                updated=True
            elif value:
                fields[field]=value
            else:
                fields.pop(field,None)
            evidence_text=details["field_evidence"].get(field)
            if value and evidence_text:
                session.add(Evidence(scholarship_id=item.id,field_name=field,value=str(value),
                    source_url=item.official_source_url,evidence_text=evidence_text,content_hash=snapshot.content_hash))
        if updated:
            item.field_data=fields
            session.flush()
            evidence_fields={e.field_name for e in session.query(Evidence).filter_by(scholarship_id=item.id).all()}
            result=verify({"fields":fields},item.official_source_url,evidence_fields)
            item.confidence_score=result["confidence_score"]
            item.confidence_status=result["confidence_status"]
            item.verification_reasons=result["reasons"]
            changed+=1
    session.commit()
    print(f"Reprocessed official PDF snapshots; records enriched: {changed}")
