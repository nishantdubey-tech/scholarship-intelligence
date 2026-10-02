"""Parser facade."""
from app.crawler.extractors import extract_page

def parse_html(html: str, url: str) -> dict:
    return extract_page(html, url)
