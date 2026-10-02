"""URL normalization and content hashing helpers."""
import hashlib
from urllib.parse import urlparse, urlunparse

def normalize_url(url: str) -> str:
    p = urlparse(url.strip())
    if p.scheme not in {"http", "https"} or not p.netloc: return ""
    return urlunparse((p.scheme.lower(), p.netloc.lower(), p.path or "/", "", p.query, ""))

def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
