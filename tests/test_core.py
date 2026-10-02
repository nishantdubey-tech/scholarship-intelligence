from app.crawler.normalize import normalize_url
from app.crawler.source_classifier import classify_source
from app.verification.confidence import score, status
from app.crawler.extractors import extract_page, extract_pages
from app.services.status import refresh_statuses
from datetime import datetime, timezone
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.db import Base
from app.models.scholarship import Scholarship, ChangeEvent
from app.change_detection.detector import detect_changes

def test_url_normalization():
    assert normalize_url("HTTPS://Example.com/a#frag") == "https://example.com/a"

def test_source_classification():
    assert classify_source("https://tribal.nic.in/x") == "GOVERNMENT"
    assert classify_source("https://scholarships.gov.in/All-Scholarships") == "SCHOLARSHIP_PORTAL"
    assert classify_source("https://example.com") == "OTHER"

def test_confidence_requires_supported_evidence():
    result, reasons=score({"fields":{"name":"Test"}},True,{"name"})
    assert result == 55
    assert "eligibility" in " ".join(reasons)
    assert status(94.9)=="REVIEW_REQUIRED"
    assert status(95)=="VERIFIED"

def test_extractor_never_fills_absent_fields():
    parsed=extract_page("<html><title>Merit Scholarship</title><h1>Merit Scholarship</h1></html>","https://example.org")
    assert parsed == {}

def test_keyword_free_page_ignored():
    assert extract_page("<title>News</title><p>hello</p>","https://example.org")=={}

def test_generic_portal_title_not_recorded():
    html="<title>Students</title><h1>Students Students</h1><p>Scholarships are available.</p>"
    assert extract_page(html,"https://scholarships.gov.in/Students")=={}

def test_nsp_index_extracts_individual_official_scheme_cards():
    html='''<button>Test Department</button><div><h6>Example Merit Scholarship Scheme (Merit Based)</h6>
    <span>Student Application Open till : 31-10-2026</span><a href="/guide.pdf">Specifications</a></div>'''
    records=extract_pages(html,"https://scholarships.gov.in/All-Scholarships")
    assert len(records)==1
    assert records[0]["fields"]["name"]=="Example Merit Scholarship Scheme (Merit Based)"
    assert records[0]["fields"]["closing_date"]=="31-10-2026"
    assert records[0]["fields"]["official_source_url"]=="https://scholarships.gov.in/guide.pdf"

def test_official_csr_record_has_only_evidenced_facts():
    html='''<title>Tata</title><h1>Updates</h1><p>Tata Capital's Pankh Scholarship programme offers support.
    Depending on their course of study, students receive scholarships covering up to 80% of tuition fees.
    The annual income of the student's family should not exceed ₹2,50,000 from all sources.</p>'''
    records=extract_pages(html,"https://www.tata.com/newsroom/community/tata-capital-pankh-scholarship")
    assert len(records)==1
    assert records[0]["fields"]["amount"] is None
    assert records[0]["fields"]["closing_date"] is None
    assert records[0]["fields"]["provider"]=="Tata Capital"

def test_health_endpoint():
    response=TestClient(app).get("/health")
    assert response.status_code==200 and response.json()=={"status":"ok"}

def test_expired_date_status_is_derived():
    class Item:
        closing_date="01 January 2020"
        current_status="ACTIVE"
        last_verified_at=datetime(2026,10,1,tzinfo=timezone.utc)
    class Query:
        def all(self): return [item]
        def __iter__(self): return iter([item])
    class FakeSession:
        def query(self, model): return Query()
    item=Item()
    assert refresh_statuses(FakeSession(),datetime(2026,10,2,tzinfo=timezone.utc))==1
    assert item.current_status=="EXPIRED"

def test_change_detection_persists_old_new_evidence():
    engine=create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine)
    with Session() as session:
        item=Scholarship(name="Evidence test",official_source_url="https://example.gov.in/guideline.pdf",amount="₹10,000")
        session.add(item);session.commit()
        assert detect_changes(session,item,{"amount":"₹12,000"},item.official_source_url,"Official page states ₹12,000") == 1
        session.commit()
        event=session.query(ChangeEvent).one()
        assert (event.old_value,event.new_value,event.evidence)==("₹10,000","₹12,000","Official page states ₹12,000")
    Base.metadata.drop_all(engine)

def test_demonstration_change_is_marked_and_does_not_mutate_record():
    engine=create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine)
    with Session() as session:
        item=Scholarship(name="Evidence test",official_source_url="https://example.gov.in/x",amount="₹10,000")
        session.add(item);session.commit()
        assert detect_changes(session,item,{"amount":"DEMO ONLY: ₹12,000"},item.official_source_url,
            "DEMONSTRATION ONLY: synthetic test; not source evidence",is_demonstration=True,
            scenario_id="test-scenario") == 1
        session.commit()
        event=session.query(ChangeEvent).one()
        assert item.amount == "₹10,000"
        assert (event.old_value,event.new_value,event.is_demonstration,event.scenario_id) == (
            "₹10,000","DEMO ONLY: ₹12,000",True,"test-scenario")
    Base.metadata.drop_all(engine)

def test_scholarship_api_confidence_filter_and_pagination():
    response=TestClient(app).get("/scholarships",params={"min_confidence":95,"page":1,"page_size":3})
    assert response.status_code==200
    data=response.json()
    assert data["page_size"]==3
    assert all(x["confidence_score"]>=95 for x in data["items"])

def test_stats_exposes_assignment_metrics():
    response=TestClient(app).get("/stats")
    assert response.status_code==200
    assert {"expiring_soon","no_longer_verifiable","recently_updated_30d"} <= response.json().keys()
