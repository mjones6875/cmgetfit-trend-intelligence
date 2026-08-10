"""
tiktok_scraper.py
-----------------
Ingestion module for TikTok public video trend data via TikTok Research API.

Uses the official TikTok Research API (academic access) to retrieve public
video metadata, engagement metrics, and hashtag data for food and wellness
content trend analysis.

IMPORTANT — ACADEMIC USE ONLY:
The TikTok Research API is granted for non-commercial academic research only.
This module must not be used in any commercial product or paid service.
Access is granted per the TikTok Research Tools Terms of Service.

Status: Pending researcher API approval.
Application submitted at: developers.tiktok.com/application/research-api

Security: API credentials loaded from environment variables. Never
hardcoded.

Author: Marlon J. Jones Jr.
"""

import os
import logging

from dotenv import load_dotenv

load_dotenv()

TIKTOK_CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY")
TIKTOK_CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET")

if not TIKTOK_CLIENT_KEY or not TIKTOK_CLIENT_SECRET:
    logging.warning(
        "TikTok Research API credentials not found. "
        "Module is inactive pending researcher access approval. "
        "Apply at developers.tiktok.com/application/research-api"
    )

# TODO (Weeks 3-4, after approval): implement fetch_tiktok_trends()
#
# 1. Authenticate using client_key and client_secret OAuth flow
# 2. Search public food and wellness videos by keyword using /research/video/query/
# 3. Extract: video titles, hashtags, view counts, like counts, comment counts
# 4. Calculate view velocity (views per day since upload) as engagement signal
# 5. Normalize output to the common ingestion schema
# 6. Store results in SQLite
#
# Reference: developers.tiktok.com/doc/research-api-get-started
