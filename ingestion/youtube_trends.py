"""
youtube_trends.py
-----------------
Ingestion module for the YouTube Data API v3.

Pulls trending food and wellness video data using broad category search
queries to conserve daily API quota (10,000 units/day, 100 units per search).
Results are normalized to the common ingestion schema and stored in SQLite.

Rate limiting: implements exponential backoff on HTTP 429 responses.
Security: API key loaded from environment variable YOUTUBE_API_KEY — never
hardcoded.

Author: Marlon J. Jones Jr.
"""

import os

from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY:
    raise EnvironmentError("YOUTUBE_API_KEY not found in environment. Check your .env file.")

# TODO (Weeks 3-4): implement fetch_youtube_trends()
