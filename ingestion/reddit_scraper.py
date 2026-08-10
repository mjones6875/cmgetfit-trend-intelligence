"""
reddit_scraper.py
------------------
Ingestion module for Reddit via PRAW.

Pulls post titles, engagement metrics, and top-level comments from target
food and wellness subreddits (see config/config_template.yaml,
target_subreddits). Filters for a minimum upvote threshold to reduce noise.

Security: REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET are loaded from the
environment — never hardcoded. Does not store raw usernames or post IDs
linking back to individual users.

Author: Marlon J. Jones Jr.
"""

import os

from dotenv import load_dotenv

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")

if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
    raise EnvironmentError(
        "REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET not found in environment. Check your .env file."
    )

# TODO (Weeks 3-4): implement fetch_reddit_posts()
