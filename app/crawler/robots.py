"""Robots.txt policy checks cached per origin."""
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from functools import lru_cache
import httpx
from app.config import USER_AGENT, REQUEST_TIMEOUT

@lru_cache(maxsize=128)
def _parser(origin: str):
    rp = RobotFileParser(); rp.set_url(origin + "/robots.txt")
    try:
        response = httpx.get(rp.url, headers={"User-Agent": USER_AGENT}, timeout=REQUEST_TIMEOUT)
        if response.status_code < 400:
            rp.parse(response.text.splitlines())
        else: rp.parse(["User-agent: *", "Disallow:"])
    except httpx.HTTPError:
        rp.parse(["User-agent: *", "Disallow: /"])
    return rp

def allowed(url: str) -> bool:
    p = urlparse(url)
    return _parser(f"{p.scheme}://{p.netloc}").can_fetch(USER_AGENT, url)
