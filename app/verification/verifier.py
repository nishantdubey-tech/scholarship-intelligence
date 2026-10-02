"""Source verification gates: only trusted source types can be verified."""
from app.crawler.source_classifier import classify_source
from app.verification.confidence import score, status

def verify(record: dict, url: str, evidence_fields: set[str]) -> dict:
    kind = classify_source(url)
    official = kind in {"GOVERNMENT", "UNIVERSITY", "CORPORATE_CSR", "FOUNDATION", "NGO_TRUST", "INTERNATIONAL", "SCHOLARSHIP_PORTAL"}
    value, reasons = score(record, official, evidence_fields)
    if not official: reasons.append("Primary source not established")
    return {"source_type": kind, "official": official, "confidence_score": value,
            "confidence_status": status(value) if official else "REVIEW_REQUIRED", "reasons": reasons}
