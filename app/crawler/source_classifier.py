"""Conservative source type classification based on domain signals."""
from urllib.parse import urlparse

def classify_source(url: str) -> str:
    host = urlparse(url).hostname or ""
    host = host.lower().removeprefix("www.")
    if host.endswith(".gov.in") or host.endswith(".nic.in") or host.endswith(".gov"):
        return "GOVERNMENT"
    if host.endswith("scholarships.reliancefoundation.org") or host.endswith("reliancefoundation.org"):
        return "FOUNDATION"
    if host.endswith("tata.com") and "scholarship" in url.lower():
        return "CORPORATE_CSR"
    if host.endswith((".ac.in", ".edu.in", ".edu")) or any(x in host for x in ("ugc.ac.in", "aicte-india.org", "university")):
        return "UNIVERSITY"
    if any(x in host for x in ("scholarships.gov.in", "scholarship.gov.in")):
        return "SCHOLARSHIP_PORTAL"
    if any(x in host for x in ("foundation", "trust.org", "org.in")):
        return "FOUNDATION"
    return "OTHER"
