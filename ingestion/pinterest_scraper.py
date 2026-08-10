"""
pinterest_scraper.py
---------------------
Ingestion module for Pinterest Trends — optional for MVP, pending
developer application approval.

Pinterest often leads other platforms by 4 to 6 weeks in food and wellness
trends, making it a high-value early signal once access is available.

Security: API key loaded from environment variable PINTEREST_API_KEY —
never hardcoded.

Author: Marlon J. Jones Jr.
"""

import os

from dotenv import load_dotenv

load_dotenv()

PINTEREST_API_KEY = os.getenv("PINTEREST_API_KEY")

if not PINTEREST_API_KEY or PINTEREST_API_KEY == "pending_approval":
    raise EnvironmentError(
        "PINTEREST_API_KEY not available yet — Pinterest developer application pending approval."
    )

# TODO (post-MVP): implement fetch_pinterest_trends() once API access is approved
