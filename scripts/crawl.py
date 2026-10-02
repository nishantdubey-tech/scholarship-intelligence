#!/usr/bin/env python3
"""Run one repeatable bounded crawl."""
import json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.services.crawler import run_crawl
print(json.dumps(run_crawl(), indent=2, default=str))
