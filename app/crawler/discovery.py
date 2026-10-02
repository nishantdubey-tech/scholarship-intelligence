"""Bounded domain-aware discovery from a compact official seed registry."""
from urllib.parse import urljoin, urlparse
import re
import httpx
from bs4 import BeautifulSoup
from app.config import USER_AGENT, REQUEST_TIMEOUT, REQUEST_DELAY, MAX_PAGES_PER_SEED, MAX_CANDIDATE_PAGES
from app.crawler.normalize import normalize_url
from app.crawler.robots import allowed
from app.crawler.source_classifier import classify_source

SEEDS = [
    "https://scholarships.gov.in/All-Scholarships",
    "https://www.ugc.gov.in/",
    "https://www.aicte-india.org/",
    "https://socialjustice.gov.in/",
    "https://tribal.nic.in/",
    "https://education.gov.in/",
    "https://www.scholarships.reliancefoundation.org/UG_Scholarship",
    "https://www.sxuk.edu.in/scholarship",
    "https://www.tata.com/newsroom/community/tata-capital-pankh-scholarship",
]
TERMS = re.compile(r"scholarship|fellowship|financial.?aid|student.?support|education.?grant", re.I)

def discover(seed_urls=None, max_pages=MAX_PAGES_PER_SEED):
    """Yield candidate links by crawling only same-origin pages and obeying robots."""
    candidates, candidate_order, visited = set(), [], set()
    def add_candidate(url):
        if url and url not in candidates:
            candidates.add(url); candidate_order.append(url)
    seeds = seed_urls or SEEDS
    for seed in seeds:
        normalized = normalize_url(seed)
        if TERMS.search(seed) and classify_source(seed) != "OTHER": add_candidate(normalized)
    headers = {"User-Agent": USER_AGENT}
    with httpx.Client(follow_redirects=True, timeout=REQUEST_TIMEOUT, headers=headers) as client:
        for seed in seeds:
            origin = f"{urlparse(seed).scheme}://{urlparse(seed).netloc}"
            queue = [normalize_url(seed)]
            for _ in range(max_pages):
                if not queue: break
                url = queue.pop(0)
                if not url or url in visited: continue
                visited.add(url)
                if not allowed(url): continue
                try:
                    response = client.get(url)
                    if response.status_code >= 400 or "html" not in response.headers.get("content-type", "").lower(): continue
                    soup = BeautifulSoup(response.text, "html.parser")
                    for a in soup.find_all("a", href=True):
                        target = normalize_url(urljoin(str(response.url), a["href"]))
                        if not target: continue
                        label = a.get_text(" ", strip=True)
                        if TERMS.search(label + " " + target) and classify_source(target) != "OTHER": add_candidate(target)
                        if target.startswith(origin) and target not in visited and len(queue) < max_pages * 3:
                            queue.append(target)
                except httpx.HTTPError:
                    continue
                import time
                time.sleep(REQUEST_DELAY)
    return candidate_order[:MAX_CANDIDATE_PAGES]
