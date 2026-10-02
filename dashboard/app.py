"""Searchable review dashboard for scholarship records and field evidence."""
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import streamlit as st
from app.database.db import initialize, SessionLocal
from app.models.scholarship import Scholarship
from app.services.status import refresh_statuses

st.set_page_config(page_title="Scholarship Intelligence", layout="wide")
initialize()
with SessionLocal() as session:
    refresh_statuses(session)
    session.commit()
    rows = session.query(Scholarship).order_by(Scholarship.name).all()


def value_text(value):
    if value is None or value == "":
        return "Not specified"
    if isinstance(value, (list, tuple)):
        return ", ".join(value_text(v) for v in value)
    if isinstance(value, dict):
        return "; ".join(f"{k}: {value_text(v)}" for k, v in value.items())
    return str(value)


def option_values(key):
    vals = set()
    for row in rows:
        data = row.field_data or {}
        val = data.get(key)
        if isinstance(val, list):
            vals.update(str(x) for x in val if x)
        elif val:
            vals.add(str(val))
    return sorted(vals, key=str.casefold)


st.title("Scholarship Intelligence")
st.caption("Primary-source listings with evidence and transparent confidence scores")
now = datetime.now(timezone.utc)
recent_cutoff = now - timedelta(days=30)
recent = sum(bool(x.updated_at and (x.updated_at.replace(tzinfo=timezone.utc) if x.updated_at.tzinfo is None else x.updated_at) >= recent_cutoff) for x in rows)
metrics = [
    ("Discovered", len(rows)),
    ("Verified ≥95%", sum(x.confidence_status == "VERIFIED" and x.confidence_score >= 95 for x in rows)),
    ("Review required", sum(x.confidence_status != "VERIFIED" for x in rows)),
    ("Active", sum(x.current_status == "ACTIVE" for x in rows)),
    ("Expiring soon", sum(x.current_status == "EXPIRING_SOON" for x in rows)),
    ("Expired", sum(x.current_status == "EXPIRED" for x in rows)),
    ("Unverifiable", sum(x.current_status == "NO_LONGER_VERIFIABLE" for x in rows)),
    ("Updated · 30 days", recent),
]
for start in (0, 4):
    cols = st.columns(4)
    for col, (label, value) in zip(cols, metrics[start:start + 4]):
        col.metric(label, value)
if rows:
    st.metric("Average confidence", f"{sum(x.confidence_score for x in rows) / len(rows):.1f}%")

with st.expander("Filters", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    search = c1.text_input("Name, provider, or keyword")
    status_options = ["All"] + sorted({x.current_status for x in rows})
    status_filter = c2.selectbox("Status", status_options)
    source_options = ["All"] + sorted({x.source_type for x in rows})
    source_filter = c3.selectbox("Source type", source_options)
    provider_options = ["All"] + sorted({x.provider for x in rows if x.provider})
    provider_filter = c4.selectbox("Provider", provider_options)

    c5, c6, c7, c8 = st.columns(4)
    education_filter = c5.selectbox("Education level", ["All"] + option_values("education_level"))
    category_filter = c6.selectbox("Category", ["All"] + option_values("category_criteria"))
    gender_filter = c7.selectbox("Gender", ["All"] + option_values("gender_criteria"))
    domicile_filter = c8.selectbox("Domicile", ["All"] + option_values("domicile_requirements"))
    confidence_range = st.slider("Confidence score", 0, 100, (0, 100))
    deadline_filter = st.selectbox("Deadline", ["Any", "Expired", "Expiring within 30 days", "More than 30 days", "No parsed deadline"])

filtered = []
for item in rows:
    data = item.field_data or {}
    haystack = " ".join([item.name or "", item.provider or "", str(item.eligibility or ""),
                         str(data.get("target_population") or "")]).casefold()
    if search and search.casefold() not in haystack:
        continue
    if status_filter != "All" and item.current_status != status_filter:
        continue
    if source_filter != "All" and item.source_type != source_filter:
        continue
    if provider_filter != "All" and item.provider != provider_filter:
        continue
    if education_filter != "All" and value_text(data.get("education_level")) != education_filter:
        continue
    if category_filter != "All" and category_filter not in ([str(v) for v in data.get("category_criteria", [])] if isinstance(data.get("category_criteria"), list) else [str(data.get("category_criteria"))]):
        continue
    if gender_filter != "All" and gender_filter != value_text(data.get("gender_criteria")):
        continue
    if domicile_filter != "All" and domicile_filter != value_text(data.get("domicile_requirements")):
        continue
    if not confidence_range[0] <= item.confidence_score <= confidence_range[1]:
        continue
    has_deadline = bool(item.closing_date)
    if deadline_filter == "No parsed deadline" and has_deadline:
        continue
    if deadline_filter == "Expired" and item.current_status != "EXPIRED":
        continue
    if deadline_filter == "Expiring within 30 days" and item.current_status != "EXPIRING_SOON":
        continue
    if deadline_filter == "More than 30 days" and (not has_deadline or item.current_status in {"EXPIRED", "EXPIRING_SOON"}):
        continue
    filtered.append(item)

st.subheader(f"Scholarships ({len(filtered)})")
for item in filtered:
    with st.expander(f"{item.name} — {item.current_status} — {item.confidence_score:.1f}%"):
        data = item.field_data or {}
        st.write({
            "Name": item.name,
            "Provider": value_text(item.provider),
            "Amount": value_text(item.amount),
            "Benefit": value_text(data.get("benefit_description")),
            "Eligibility": value_text(item.eligibility),
            "Academic requirements": value_text(data.get("academic_requirements")),
            "Education level": value_text(data.get("education_level")),
            "Course requirements": value_text(data.get("course_requirements")),
            "Income criteria": value_text(data.get("income_criteria")),
            "Age criteria": value_text(data.get("age_criteria")),
            "Gender criteria": value_text(data.get("gender_criteria")),
            "Category criteria": value_text(data.get("category_criteria")),
            "Domicile": value_text(data.get("domicile_requirements")),
            "Institution requirements": value_text(data.get("institution_requirements")),
            "Opening date": value_text(data.get("opening_date")),
            "Closing date": value_text(item.closing_date),
            "Documents required": value_text(data.get("documents_required")),
            "Selection process": value_text(data.get("selection_process")),
            "Renewal requirements": value_text(data.get("renewal_requirements")),
            "Target population": value_text(data.get("target_population")),
        })
        st.markdown(f"[Official source]({item.official_source_url})")
        if item.application_url:
            st.markdown(f"[Application link]({item.application_url})")
        st.write({"Source type": item.source_type, "Current status": item.current_status,
                  "Confidence score": item.confidence_score, "Confidence status": item.confidence_status,
                  "Why this score": item.verification_reasons, "Last verified": item.last_verified_at})
        st.subheader("Field evidence")
        if item.evidence:
            for evidence in item.evidence:
                st.write({"field": evidence.field_name, "value": evidence.value,
                          "excerpt": evidence.evidence_text, "source": evidence.source_url,
                          "retrieved_at": evidence.retrieved_at, "content_hash": evidence.content_hash})
        else:
            st.info("No field-level evidence is stored for this record.")
        st.subheader("Change history")
        if item.history:
            for event in item.history:
                if event.is_demonstration:
                    st.warning(f"DEMONSTRATION ONLY — {event.scenario_id}; not an observed source change")
                st.write({"field": event.field_name, "old value": event.old_value,
                          "new value": event.new_value, "detected at": event.detected_at,
                          "source": event.source_url, "evidence": event.evidence})
        else:
            st.caption("No change events are recorded for this scholarship.")
