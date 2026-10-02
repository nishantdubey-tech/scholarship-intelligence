"""Record field changes as append-only history events."""
from __future__ import annotations
from app.models.scholarship import ChangeEvent

def detect_changes(session, scholarship, incoming: dict, url: str, evidence: str,
                   is_demonstration: bool = False, scenario_id: str | None = None) -> int:
    """Append value changes; demonstration events never mutate the real record."""
    if is_demonstration and not scenario_id:
        raise ValueError("Demonstration changes require a scenario_id")
    changes = 0
    for field, value in incoming.items():
        if not hasattr(scholarship, field) or value is None: continue
        old = getattr(scholarship, field)
        # A first observed value is enrichment, not a detected change. Only compare
        # fields that previously had a source-backed value.
        if old is not None and old != value:
            session.add(ChangeEvent(scholarship_id=scholarship.id, field_name=field,
                old_value=str(old), new_value=str(value), source_url=url, evidence=evidence,
                is_demonstration=is_demonstration, scenario_id=scenario_id))
            if not is_demonstration:
                setattr(scholarship, field, value)
            changes += 1
        elif old is None:
            setattr(scholarship, field, value)
    return changes
