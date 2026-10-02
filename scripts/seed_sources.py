#!/usr/bin/env python3
"""Print the configured seed registry; no synthetic scholarship rows are created."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.crawler.discovery import SEEDS
for url in SEEDS: print(url)
