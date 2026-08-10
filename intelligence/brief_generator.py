"""
brief_generator.py
--------------------
Generates the weekly content brief by passing the top 5 trend clusters and
their supporting data to the Anthropic Claude API (claude-sonnet-4-6).

Prompt inputs: trend cluster name, supporting entities, trend score
components, sentiment classification, source distribution, estimated weeks
until peak, brand voice context.

Brief output per trend: what the trend is and why it's rising, 3 specific
content angles, relevant hashtags, suggested posting window, and a
confidence rating (High / Medium / Low) based on signal strength. When
fewer than 3 trends have strong cross-platform signals, the brief flags a
low-confidence week rather than fabricating recommendations.

Security: API key loaded from environment variable ANTHROPIC_API_KEY —
never hardcoded, never logged.

Author: Marlon J. Jones Jr.
"""

import os

from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    raise EnvironmentError("ANTHROPIC_API_KEY not found in environment. Check your .env file.")

# TODO (Weeks 9-10): implement generate_brief()
