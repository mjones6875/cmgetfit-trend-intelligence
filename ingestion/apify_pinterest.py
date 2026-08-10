"""
apify_pinterest.py
------------------
Ingestion module for Pinterest Trends data via Apify.

Uses the Apify platform's Pinterest Trends Scraper actor
(automation-lab/pinterest-trends-scraper) to extract trending keywords,
growth scores, and seasonality data from Pinterest Trends.

Why Apify instead of the official Pinterest API: the official Pinterest
Developer API does not expose Pinterest Trends data — it's built for ad
buyers and content managers, not for reading trend signals. Apify provides
legitimate programmatic access to Pinterest Trends, which is the actual
data source used by marketers and researchers for trend analysis.

Rate limiting: Apify manages rate limiting internally via its Actor
infrastructure. The free tier includes monthly credits sufficient for
weekly pipeline runs.

Security: API token loaded from environment variable APIFY_API_KEY —
never hardcoded.

Author: Marlon J. Jones Jr.
"""

import os

from dotenv import load_dotenv

load_dotenv()

APIFY_API_KEY = os.getenv("APIFY_API_KEY")
PINTEREST_TRENDS_ACTOR = "automation-lab/pinterest-trends-scraper"

if not APIFY_API_KEY:
    raise EnvironmentError(
        "APIFY_API_KEY not found in environment. "
        "Sign up at apify.com and get your token from "
        "console.apify.com/settings/integrations"
    )

# TODO (Weeks 3-4): implement fetch_pinterest_trends()
#
# from apify_client import ApifyClient
#
# client = ApifyClient(APIFY_API_KEY)
#
# run_input = {
#     "keywords": ["recipe", "meal prep", "healthy food"],
#     "country": "US",
#     "limit": 50,
# }
#
# run = client.actor(PINTEREST_TRENDS_ACTOR).call(run_input=run_input)
#
# for item in client.dataset(run["defaultDatasetId"]).iterate_items():
#     # normalize to the common ingestion schema and store in SQLite
#     pass
