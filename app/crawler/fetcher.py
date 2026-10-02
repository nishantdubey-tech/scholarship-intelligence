"""Resilient HTTP fetch helper."""
import time
import httpx
from app.config import USER_AGENT, REQUEST_TIMEOUT

def fetch(url: str, retries: int = 1):
    headers = {"User-Agent": USER_AGENT}
    for attempt in range(retries + 1):
        try:
            response = httpx.get(url, headers=headers, timeout=REQUEST_TIMEOUT, follow_redirects=True)
            response.raise_for_status()
            return response
        except httpx.HTTPError:
            if attempt == retries: raise
            time.sleep(2 ** attempt)
