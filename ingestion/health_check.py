"""
health_check.py
----------------
Verifies each configured data source is reachable before a pipeline run.

For sources that require an API key, this only confirms the key is present
in the environment — it deliberately does not make a live authenticated
call, since a present-but-invalid key should fail loudly inside that
source's own ingestion module rather than being silently reported healthy
here.

Google Trends (pytrends) requires no key, so it gets an inexpensive live
request as its actual availability signal.

Author: Marlon J. Jones Jr.
"""

import logging
import os

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

REQUIRED_ENV_VARS = {
    "youtube": ["YOUTUBE_API_KEY"],
    "news_api": ["NEWS_API_KEY"],
    "anthropic": ["ANTHROPIC_API_KEY"],
    "reddit": ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET"],
    "pinterest": ["PINTEREST_API_KEY"],
    "airtable": ["AIRTABLE_API_KEY", "AIRTABLE_BASE_ID"],
}


def _check_env_vars(source: str, var_names: list) -> bool:
    missing = [name for name in var_names if not os.getenv(name)]
    if missing:
        logger.warning("%s: missing %s", source, ", ".join(missing))
        return False
    return True


def _check_google_trends() -> bool:
    try:
        from pytrends.request import TrendReq

        TrendReq(hl="en-US", tz=360).build_payload(["food"], timeframe="now 1-d")
        return True
    except Exception as exc:  # pytrends can raise several unrelated exception types
        logger.warning("google_trends: unreachable — %s", exc)
        return False


def run_health_check() -> bool:
    """Returns True only if every configured source is healthy."""
    results = {"google_trends": _check_google_trends()}
    results.update(
        {source: _check_env_vars(source, var_names) for source, var_names in REQUIRED_ENV_VARS.items()}
    )

    for source, ok in results.items():
        logger.info("%s: %s", source, "OK" if ok else "FAILED")

    return all(results.values())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_health_check()
