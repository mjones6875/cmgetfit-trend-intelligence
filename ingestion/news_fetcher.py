"""
news_fetcher.py
----------------
Ingestion module for News API.

Pulls food and wellness news headlines and article summaries. Mainstream
media coverage of a food topic is treated as a confirmation signal for
trends already identified by Reddit and Google Trends.

Security: API key loaded from environment variable NEWS_API_KEY — never
hardcoded. Free tier is limited to 100 requests/day and development use only
(see licensing notes for commercial deployment).

Author: Marlon J. Jones Jr.
"""

import os

from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not NEWS_API_KEY:
    raise EnvironmentError("NEWS_API_KEY not found in environment. Check your .env file.")

# TODO (Weeks 3-4): implement fetch_news()
