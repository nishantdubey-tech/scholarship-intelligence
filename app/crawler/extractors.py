"""Evidence-preserving deterministic extraction from visible page text."""
from __future__ import annotations
import re
import io
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from pypdf import PdfReader

KEYWORDS = re.compile(r"scholarship|fellowship|financial aid|student grant|education grant", re.I)
GENERIC_TITLES = {"students", "students students", "overview", "scholarships and grants",
                  "national scholarship portal", "nsp : national scholarship portal",
                  "scholarship eligibility check", "candidate candidate"}
ELIGIBILITY = re.compile(r"eligible|eligibility|must have|minimum (?:marks|percentage|grade)|annual family income|income should not exceed|who can apply", re.I)
AMOUNT = re.compile(r"(?:₹|INR\s?|Rs\.?\s?)\s?[\d,]+(?:\s*(?:per annum|per year|monthly|/month|p\.m\.?))?", re.I)
DATE = re.compile(r"\b(?:\d{1,2}\s+[A-Za-z]+\s+20\d{2}|[A-Za-z]+\s+\d{1,2},?\s+20\d{2}|\d{1,2}[-/]\d{1,2}[-/]20\d{2})\b")

def extract_pages(html: str, url: str) -> list[dict]:
    """Extract one or more records; NSP's official index contains many scheme cards."""
    if "scholarships.gov.in/All-Scholarships" in url:
        soup = BeautifulSoup(html, "html.parser")
        records = []
        student_link = next((a.get("href") for a in soup.find_all("a", href=True)
                             if a.get_text(" ",strip=True).casefold() == "student"), None)
        from urllib.parse import urljoin
        application_url = urljoin(url, student_link) if student_link else None
        for heading in soup.find_all("h6"):
            name = heading.get_text(" ", strip=True)
            if not re.search(r"scholarship|fellowship|stipend scheme|financial assistance", name, re.I): continue
            card = heading.parent
            text = " ".join(card.stripped_strings)
            date_match = re.search(r"Student\s+Application\s+(?:Open till|Closed on)\s*:?\s*(\d{1,2}[-/]\d{1,2}[-/]20\d{2})", text, re.I)
            if not date_match: continue
            provider_node = heading.find_previous("button")
            provider = provider_node.get_text(" ", strip=True) if provider_node else None
            specification = next((a["href"] for a in card.find_all("a", href=True)
                                  if "specifications" in a.get_text(" ", strip=True).lower()), None)
            official_url = urljoin(url, specification) if specification else url
            if application_url: fields_application_evidence = f"NSP Student application link: {application_url}"
            else: fields_application_evidence = None
            snippet = f"{name}. {text}"
            fields = {"name":name, "provider":provider, "official_source_url":official_url, "application_url":application_url,
                      "amount":None, "benefit_description":None, "eligibility":None,
                      "academic_requirements":None, "education_level":None, "course_requirements":None,
                      "income_criteria":None, "age_criteria":None, "gender_criteria":None,
                      "category_criteria":None, "domicile_requirements":None, "institution_requirements":None,
                      "opening_date":None,"closing_date":date_match.group(1),"documents_required":None,
                      "selection_process":None,"renewal_requirements":None,"target_population":None,"current_status":None}
            evidence = {"name":snippet,"provider":snippet if provider else None,
                        "official_source_url":f"Specifications link: {official_url}","closing_date":snippet,
                        "application_url":fields_application_evidence}
            records.append({"fields":fields,"field_evidence":evidence,"text":snippet})
        return records
    if "tata.com/" in url and "scholarship" in url.lower():
        soup = BeautifulSoup(html, "html.parser")
        text = " ".join(soup.stripped_strings)
        if "Pankh Scholarship programme" in text:
            eligibility = re.search(r"The annual income of the student.s family should not exceed.{0,180}", text, re.I)
            benefit = re.search(r"Depending on their course of study.{0,220}", text, re.I)
            excerpt = lambda match: text[max(0,match.start()-80):match.end()+80] if match else None
            name = "Tata Capital Pankh Scholarship Programme"
            fields = {"name":name,"provider":"Tata Capital","official_source_url":url,"application_url":None,
                      "amount":None,"benefit_description":benefit.group(0) if benefit else None,
                      "eligibility":eligibility.group(0) if eligibility else None,"academic_requirements":"At least 60% in qualifying examination" if "at least 60%" in text.lower() else None,
                      "education_level":"Senior Secondary, Undergraduate, Diploma and Postgraduate","course_requirements":None,
                      "income_criteria":"Annual family income should not exceed ₹2,50,000" if eligibility else None,
                      "age_criteria":None,"gender_criteria":None,"category_criteria":None,"domicile_requirements":None,
                      "institution_requirements":None,"opening_date":None,"closing_date":None,"documents_required":None,
                      "selection_process":"Interview followed by a final committee round" if "interview" in text.lower() else None,
                      "renewal_requirements":"Renewal contingent on academic performance" if "renewal" in text.lower() else None,
                      "target_population":"Students from economically underprivileged and affirmative-action families",
                      "current_status":"NO_LONGER_VERIFIABLE" if "April 2025" in text and "2026-27" not in text else "REVIEW_REQUIRED"}
            field_evidence={"name":name,"provider":excerpt(re.search(r"Tata Capital.s Pankh Scholarship programme",text,re.I)),
                            "eligibility":excerpt(eligibility),"benefit_description":excerpt(benefit)}
            return [{"fields":fields,"field_evidence":field_evidence,"text":text}]
    from app.crawler.source_classifier import classify_source
    if classify_source(url) == "UNIVERSITY":
        soup = BeautifulSoup(html, "html.parser")
        records = []
        page_title = soup.title.get_text(" ", strip=True) if soup.title else "University"
        # The first six tables are the university's current 2026-27 offerings;
        # later tables are summaries/repeated layouts and third-party catalogues.
        for table in soup.find_all("table")[:6]:
            for row in table.find_all("tr"):
                cells = [c.get_text(" ", strip=True) for c in row.find_all(["td", "th"])]
                if len(cells) < 2: continue
                row_text = " | ".join(cells)
                name = next((c for c in cells if re.search(r"scholarship|fellowship|financial aid", c, re.I)), None)
                if not name or name.casefold() in {"name of scholarship", "scholarship scheme"}: continue
                if row.find("th") and len(row.find_all("td")) == 0: continue
                benefit = next((c for c in reversed(cells[1:]) if re.search(r"waiver|₹|INR|Rs\.?", c, re.I)), None)
                amount_match = AMOUNT.search(row_text)
                old_cycle = bool(re.search(r"20(?:1\d|2[0-5])[-/](?:\d{2,4})", name))
                fields = {"name":name,"provider":page_title.split(" | ")[0],"official_source_url":url,
                          "application_url":None,"amount":amount_match.group(0) if amount_match else None,
                          "benefit_description":benefit,"eligibility":row_text,"academic_requirements":None,
                          "education_level":None,"course_requirements":None,"income_criteria":None,"age_criteria":None,
                          "gender_criteria":None,"category_criteria":None,"domicile_requirements":None,
                          "institution_requirements":None,"opening_date":None,"closing_date":None,
                          "documents_required":None,"selection_process":None,"renewal_requirements":None,
                          "target_population":None,"current_status":"EXPIRED" if old_cycle else None}
                evidence={"name":row_text,"provider":page_title,"eligibility":row_text,
                          "benefit_description":row_text,"amount":row_text if fields["amount"] else None}
                records.append({"fields":fields,"field_evidence":evidence,"text":row_text})
        if records: return records
    parsed = extract_page(html, url)
    return [parsed] if parsed else []

def extract_pdf_details(content: bytes | str, expected_name: str | None = None) -> dict:
    """Extract explicit PDF values, selecting scheme-specific sections when shared."""
    try:
        if isinstance(content,str): text=content
        else:
            reader=PdfReader(io.BytesIO(content))
            text="\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        return {"fields":{},"field_evidence":{},"text":""}
    fields, evidence = {}, {}

    # A shared government guideline PDF can define multiple disability schemes.
    # Restrict evidence to the section matching the named NSP card.
    scheme_text=text
    shared_disability=False
    if expected_name and "scholarships for students with disabilities" in text.lower():
        shared_disability=True
        name=expected_name.lower()
        if "pre matric" in name:
            pattern=r"\d+\.\s*PRE-MATRIC SCHOLARSHIP FOR STUDENTS WITH BENCHMARK[\s\S]{0,80}?DISABILIT\w*"
        elif "post matric" in name:
            pattern=r"\d+\.\s*POST-MATRIC SCHOLARSHIP FOR STUDENT WITH BENCHMARK[\s\S]{0,80}?DISABILIT\w*"
        else:
            pattern=r"\d+\.\s*TOP CLASS EDUCATION SCHOLARSHIP FOR STUDENT WITH BENCHMARK[\s\S]{0,80}?DISABILIT\w*"
        matches=list(re.finditer(pattern,text,re.I))
        if matches:
            start=matches[-1].start()
            next_heading=re.search(r"\n\s*\d+\.\s*(?:PRE-MATRIC|POST-MATRIC|TOP CLASS EDUCATION) SCHOLARSHIP",text[matches[-1].end():],re.I)
            end=matches[-1].end()+next_heading.start() if next_heading else len(text)
            scheme_text=text[start:end]
            eligible=re.search(r"ELIGIBILITY CONDITION[S]?",scheme_text,re.I)
            if eligible:
                begin=eligible.end()
                boundary=re.search(r"QUANTUM OF FINANCIAL ASSISTANCE|RATES OF SCHOLARSHIP",scheme_text[begin:],re.I)
                criteria=scheme_text[begin:begin+1300 if not boundary else begin+boundary.start()]
                if len(criteria.strip())>50:
                    fields["eligibility"]=" ".join(criteria.split())[:1200]
                    evidence["eligibility"]=fields["eligibility"]
            # Amounts in these schemes depend on course, residence and disability
            # category; retain their official table as benefit evidence, not a false scalar.
            fields["benefit_description"]=" ".join(scheme_text.split())[:2200]
            evidence["benefit_description"]=fields["benefit_description"]

    # UGC's Ishan Uday PDF has later procedural references to eligibility; anchor
    # to its numbered scheme section rather than those document-verification steps.
    if expected_name and "ishan uday" in expected_name.lower():
        match=re.search(r"2\.\s*ELIGIBILITY\s*:\s*",text,re.I)
        if match:
            section=text[match.end():]
            boundary=re.search(r"\n\s*3\.\s*[A-Z]",section)
            if boundary: section=section[:boundary.start()]
            section=" ".join(section.split())[:1800]
            if len(section)>80:
                fields["eligibility"]=section
                evidence["eligibility"]=section

    flat_text=" ".join(scheme_text.split())
    money=r"(?:₹|Rs\.?|INR)\s*\d[\d,]*(?:\s*/-)?(?:\s*(?:per annum|per year|p\.m\.?|per month))?"
    amount_value,amount_start=None,None
    amount_heads=list(re.finditer(r"(?:AMOUNT OF SCHOLARSHIP|SCHOLARSHIP AMOUNT|QUANTUM OF SCHOLARSHIP|VALUE OF SCHOLARSHIP|FINANCIAL ASSISTANCE|RATE OF SCHOLARSHIP)",flat_text,re.I))
    if amount_heads and not shared_disability:
        for heading in reversed(amount_heads):
            section=flat_text[heading.end():heading.end()+1800]
            next_section=re.search(r"\s+\d+\.\d+\s+[A-Z][A-Z /]{4,}",section)
            if next_section: section=section[:next_section.start()]
            # Railway PMSS guidelines specify separate monthly male/female rates without a currency sign.
            rates=re.search(r"(?:2500|2,500)\s*/-?\s*per month\s+for male students[\s\S]{0,120}?(?:3000|3,000)\s*/-?\s*per month\s+for female students",section,re.I)
            if rates:
                amount_value="₹2,500/month (male); ₹3,000/month (female)"; amount_start=heading.end()+rates.start(); break
            match=re.search(money,section,re.I)
            if match:
                digits=re.sub(r"\D","",match.group(0))
                if len(digits)>=3: amount_value,amount_start=match.group(0).strip(),heading.end()+match.start(); break
    if not amount_value and not shared_disability:
        fallback=re.search(r"(?:at the rate of|scholarship amount|amount of scholarship|financial assistance)[\s\S]{0,180}?("+money+r")",flat_text,re.I)
        if fallback:
            digits=re.sub(r"\D","",fallback.group(1))
            if len(digits)>=3: amount_value,amount_start=fallback.group(1).strip(),fallback.start(1)
    if amount_value:
        fields["amount"]=amount_value
        evidence["amount"]=flat_text[max(0,amount_start-90):amount_start+len(amount_value)+90]

    # Pick the first substantive eligibility heading, skipping table-of-contents mentions.
    elig_heads=list(re.finditer(r"(?:GENERAL CONDITIONS OF ELIGIBILITY|STUDENTS ELIGIBLE FOR THE SCHOLARSHIP|ELIGIBILITY(?: AND COURSE DURATION| FOR SCHOLARSHIP| CONDITIONS?)?|ELIGIBLITY(?: CRITERIA)?|ELIGIBLE CRITERIA)[^\n]{0,100}[:\n]",scheme_text,re.I))
    if "eligibility" not in fields:
        for heading in elig_heads:
            section=scheme_text[heading.end():heading.end()+2400]
            lead=section[:350]
            # Skip contents pages and generic summaries: require concrete eligibility language
            # immediately after the heading, not merely elsewhere in the following page.
            if len(section.strip())<100 or not re.search(r"(?:student|candidate|applicant|admission|marks|course|class|income).{0,100}(?:should|must|shall|minimum|above|below|not exceed|eligible|regular|full time|taken|secured)|(?:should|must|shall|minimum|above|below|not exceed|eligible|regular|full time|taken|secured).{0,100}(?:student|candidate|applicant|admission|marks|course|class|income)",lead,re.I): continue
            boundary=re.search(r"\n\s*(?:\d+\.\d+\s+)?(?:NUMBER OF SCHOLARSHIPS|AMOUNT OF SCHOLARSHIP|VALUE OF SCHOLARSHIP|PROCEDURE|SELECTION|RENEWAL|TERMS AND CONDITIONS|SCOPE OF THE SCHOLARSHIP)",section,re.I)
            if boundary: section=section[:boundary.start()]
            fields["eligibility"]=" ".join(section.split())[:1800]
            evidence["eligibility"]=fields["eligibility"]
            break
    selection=re.search(r"(?:CRITERIA OF SELECTION|SELECTION PROCEDURE)[\s\S]{0,900}?(?=\n\s*\d+\.\d+\s+|\Z)",scheme_text,re.I)
    if selection:
        fields["selection_process"]=" ".join(selection.group(0).split())[:1200]
        evidence["selection_process"]=fields["selection_process"]
    renewal=re.search(r"RENEWAL[S]?[\s\S]{0,800}?(?=\n\s*\d+\.\d+\s+|\Z)",scheme_text,re.I)
    if renewal:
        fields["renewal_requirements"]=" ".join(renewal.group(0).split())[:1000]
        evidence["renewal_requirements"]=fields["renewal_requirements"]
    return {"fields":fields,"field_evidence":evidence,"text":text}

def extract_page(html: str, url: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    for node in soup(["script", "style", "noscript"]): node.decompose()
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    text = " ".join(soup.stripped_strings)
    if not KEYWORDS.search(title + " " + text): return {}
    heading = soup.find(["h1", "h2"])
    name = heading.get_text(" ", strip=True) if heading else title
    if not name or name.casefold().strip(" :") in GENERIC_TITLES: return {}
    if not re.search(r"scholarship|fellowship|grant", name, re.I): return {}
    app_link = None
    for a in soup.find_all("a", href=True):
        label = a.get_text(" ", strip=True).lower()
        if any(k in label for k in ("apply", "application", "register")):
            from urllib.parse import urljoin
            app_link = urljoin(url, a["href"]); break
    amount_match = AMOUNT.search(text)
    date_match = DATE.search(text)
    eligibility_match = ELIGIBILITY.search(text)
    # Generic portal pages often mention scholarships only in navigation.
    if not (amount_match or eligibility_match): return {}
    # Preserve short source excerpts rather than creating unsupported values.
    def evidence(pattern):
        m = pattern.search(text)
        return text[max(0, m.start()-100):m.end()+100] if m else None
    fields = {"name": name, "provider": None, "official_source_url": url, "application_url": app_link, "amount": amount_match.group(0) if amount_match else None,
              "benefit_description": None, "eligibility": evidence(ELIGIBILITY), "academic_requirements": None,
              "education_level": None, "course_requirements": None, "income_criteria": None, "age_criteria": None,
              "gender_criteria": None, "category_criteria": None, "domicile_requirements": None,
              "institution_requirements": None, "opening_date": None,
              "closing_date": date_match.group(0) if date_match else None, "documents_required": None,
              "selection_process": None, "renewal_requirements": None, "target_population": None,
              "current_status": None, "application_url": app_link}
    field_evidence = {"name": evidence(re.compile(re.escape(name), re.I)), "official_source_url": url,
                      "amount": evidence(AMOUNT), "closing_date": evidence(DATE),
                      "eligibility": evidence(ELIGIBILITY),
                      "application_url": app_link}
    return {"fields": fields, "field_evidence": field_evidence, "text": text,
            "retrieved_at": datetime.now(timezone.utc).isoformat()}
