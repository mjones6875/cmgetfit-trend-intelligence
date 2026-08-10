"""
airtable_pusher.py
--------------------
Pushes the generated weekly brief to Airtable so it appears in the
CMgetFit Business Command Center every Monday morning.

Security: API key and base ID loaded from environment variables
AIRTABLE_API_KEY and AIRTABLE_BASE_ID — never hardcoded, never logged.

Author: Marlon J. Jones Jr.
"""

import os

from dotenv import load_dotenv

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
    raise EnvironmentError(
        "AIRTABLE_API_KEY / AIRTABLE_BASE_ID not found in environment. Check your .env file."
    )

# TODO (Weeks 9-10): implement push_to_airtable()
