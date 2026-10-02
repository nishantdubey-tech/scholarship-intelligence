"""Derive expiration and verification freshness without guessing deadlines."""
from datetime import datetime, timezone, timedelta
from dateutil import parser as date_parser
from app.models.scholarship import Scholarship

def refresh_statuses(session, now=None, stale_days=45):
    now = now or datetime.now(timezone.utc); changed = 0
    for item in session.query(Scholarship):
        verified_at = item.last_verified_at
        if verified_at and verified_at.tzinfo is None: verified_at = verified_at.replace(tzinfo=timezone.utc)
        source_status = (getattr(item,"field_data",None) or {}).get("current_status")
        status = "NO_LONGER_VERIFIABLE" if not verified_at or now-verified_at > timedelta(days=stale_days) else "ACTIVE"
        if source_status in {"EXPIRED", "NO_LONGER_VERIFIABLE", "REVIEW_REQUIRED"}: status = source_status
        if item.closing_date:
            try:
                deadline = date_parser.parse(item.closing_date, dayfirst=True)
                if deadline.tzinfo is None: deadline = deadline.replace(tzinfo=timezone.utc)
                if deadline < now: status = "EXPIRED"
                elif deadline < now + timedelta(days=30): status = "EXPIRING_SOON"
            except (ValueError, OverflowError, TypeError):
                pass
        if item.current_status != status: item.current_status=status; changed+=1
    return changed
