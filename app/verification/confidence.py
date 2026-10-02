"""Deterministic completeness and provenance score (0-100)."""
CRITICAL = ("name", "provider", "amount", "eligibility", "closing_date", "application_url")

def score(record: dict, official: bool, evidence_fields: set[str]) -> tuple[float, list[str]]:
    reasons = []
    fields = record.get("fields", {})
    points = 0.0
    if official: points += 35
    else: reasons.append("Source domain is not positively classified as official")
    if fields.get("name") and "name" in evidence_fields: points += 20
    else: reasons.append("Scholarship name lacks source evidence")
    supported = []
    for field in CRITICAL[1:]:
        value = fields.get(field)
        if not value or field not in evidence_fields:
            continue
        # A currency symbol, punctuation, or a heading alone is not amount evidence.
        if field == "amount" and len("".join(ch for ch in str(value) if ch.isdigit())) < 3:
            continue
        if field == "eligibility" and len(str(value).strip()) < 60:
            continue
        if field == "closing_date" and len(str(value).strip()) < 8:
            continue
        if field == "application_url" and not str(value).startswith(("https://", "http://")):
            continue
        supported.append(field)
    points += 45 * len(supported) / len(CRITICAL[1:])
    missing = [f for f in CRITICAL[1:] if f not in supported]
    if missing: reasons.append("Critical fields absent or unsupported: " + ", ".join(missing))
    return round(points, 1), reasons

def status(value: float) -> str:
    return "VERIFIED" if value >= 95 else "REVIEW_REQUIRED"
