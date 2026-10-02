#!/usr/bin/env python3
"""Append two explicitly labeled change-detector examples without editing a real record."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.change_detection.detector import detect_changes
from app.database.db import SessionLocal, initialize
from app.models.scholarship import ChangeEvent, Scholarship

SCENARIO_ID = "assignment-demo-v1"
DEMO_EVIDENCE = (
    "DEMONSTRATION ONLY: synthetic value used to demonstrate change-history behavior. "
    "This is not a source observation and must not be treated as scholarship information."
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record-id", type=int, default=3, help="Existing real record to attach the demo events to")
    args = parser.parse_args()
    initialize()

    with SessionLocal() as session:
        prior_events = session.query(ChangeEvent).filter_by(scenario_id=SCENARIO_ID).all()
        if len(prior_events) >= 2:
            print(f"Scenario {SCENARIO_ID} already contains two demonstration events; no changes made.")
            return
        item = session.get(Scholarship, args.record_id)
        if not item:
            raise SystemExit(f"No scholarship record {args.record_id}; crawl official sources first.")
        if not item.amount or not item.closing_date:
            raise SystemExit("Chosen real record lacks amount or deadline; select a record with both fields.")

        demo_changes = {
            "closing_date": "DEMO ONLY: 15-11-2026 (synthetic test value)",
            "amount": "DEMO ONLY: ₹55,000 (synthetic test value)",
        }
        already_recorded = {event.field_name for event in prior_events}
        pending = {key: value for key, value in demo_changes.items() if key not in already_recorded}
        created = detect_changes(
            session, item, pending, item.official_source_url, DEMO_EVIDENCE,
            is_demonstration=True, scenario_id=SCENARIO_ID,
        )
        session.commit()
        print(f"Recorded {created} DEMONSTRATION ONLY events for real record {item.id} ({item.name}).")
        print("The scholarship record itself was not modified; the new values are not source facts.")


if __name__ == "__main__":
    main()
