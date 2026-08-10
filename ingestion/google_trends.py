"""
google_trends.py
-----------------
Ingestion module for Google Trends via pytrends.

No API key required. Returns search volume time series for a given keyword,
used as the primary velocity signal in trend scoring (see
intelligence/trend_scorer.py). Can retrieve up to 5 years of history for
backtesting.

Rate limiting: pytrends is an unofficial interface to Google Trends — there
is no published rate limit, but excessive requests can trigger temporary
IP-level throttling. Space requests out and retry with backoff on failure.

Author: Marlon J. Jones Jr.
"""

# TODO (Weeks 3-4): implement fetch_google_trends()
