"""Streamlit searchable dashboard for stored, source-linked records."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import streamlit as st
from app.database.db import initialize, SessionLocal
from app.models.scholarship import Scholarship
from app.services.status import refresh_statuses

st.set_page_config(page_title="Scholarship Intelligence", layout="wide")
initialize()
with SessionLocal() as s: refresh_statuses(s); s.commit()
st.title("Scholarship Intelligence")
with SessionLocal() as s:
    rows=s.query(Scholarship).order_by(Scholarship.name).all()
    st.metric("Total discovered",len(rows))
    cols=st.columns(5)
    for col,label,pred in zip(cols,["Verified","Review required","Active","Expired","Average confidence"],
        [lambda x:x.confidence_status=="VERIFIED",lambda x:x.confidence_status!="VERIFIED",lambda x:x.current_status=="ACTIVE",lambda x:x.current_status=="EXPIRED",None]):
        col.metric(label,round(sum(x.confidence_score for x in rows)/len(rows),1) if pred is None and rows else (sum(pred(x) for x in rows) if pred else 0))
    q=st.text_input("Search scholarships or providers")
    types=sorted({x.source_type for x in rows})
    selected=st.multiselect("Source type",types)
    for item in rows:
        if q and q.casefold() not in ((item.name or "")+(item.provider or "")).casefold(): continue
        if selected and item.source_type not in selected: continue
        with st.expander(f"{item.name} — {item.current_status} — {item.confidence_score}%"):
            st.write({"Provider":item.provider,"Amount":item.amount,"Eligibility":item.eligibility,"Deadline":item.closing_date,
                      "Source type":item.source_type,"Confidence status":item.confidence_status,
                      "Why this score":item.verification_reasons,"Last verified":item.last_verified_at})
            st.markdown(f"[Official source]({item.official_source_url})")
            if item.application_url: st.markdown(f"[Application]({item.application_url})")
            st.subheader("Field evidence")
            for ev in item.evidence: st.write({"field":ev.field_name,"value":ev.value,"excerpt":ev.evidence_text,"source":ev.source_url})
            st.subheader("Change history")
            for event in item.history: st.write({"field":event.field_name,"old":event.old_value,"new":event.new_value,"detected":event.detected_at,"source":event.source_url})
