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

Reddit is marked optional: researcher access is still pending approval,
so a missing Reddit key should not fail the overall health check — the
pipeline is expected to run without it using the other sources.

Author: Marlon J. Jones Jr.
"""

import logging
import os

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# source -> (list of required env var names, whether the source is required for overall health)
SOURCES = {
    "youtube": (["YOUTUBE_API_KEY"], True),
    "news_api": (["NEWS_API_KEY"], True),
    "anthropic": (["ANTHROPIC_API_KEY"], True),
    "apify_pinterest": (["APIFY_API_KEY"], True),
    "airtable": (["AIRTABLE_API_KEY", "AIRTABLE_BASE_ID"], True),
    "reddit": (["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET"], False),
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
    """Returns True if every *required* source is healthy. Optional sources
    (currently just Reddit, pending approval) are logged but don't block
    overall health."""
    ok = True

    google_trends_ok = _check_google_trends()
    logger.info("google_trends: %s", "OK" if google_trends_ok else "FAILED")
    ok = ok and google_trends_ok

    for source, (var_names, required) in SOURCES.items():
        source_ok = _check_env_vars(source, var_names)
        status = "OK" if source_ok else ("FAILED" if required else "UNAVAILABLE (optional)")
        logger.info("%s: %s", source, status)
        if required:
            ok = ok and source_ok

    return ok


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_health_check()
