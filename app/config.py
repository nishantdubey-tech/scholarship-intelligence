"""Application settings loaded from environment variables."""
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{ROOT / 'data' / 'scholarships.db'}")
USER_AGENT = os.getenv("CRAWLER_USER_AGENT", "ScholarshipIntelligenceBot/1.0 (+local research crawler)")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "8"))
REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", "1.5"))
MAX_PAGES_PER_SEED = int(os.getenv("MAX_PAGES_PER_SEED", "4"))
MAX_CANDIDATE_PAGES = int(os.getenv("MAX_CANDIDATE_PAGES", "30"))
