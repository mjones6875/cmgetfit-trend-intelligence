"""
text_preprocessor.py
---------------------
Cleans and normalizes raw text from all ingestion sources before NLP
processing: lowercasing, URL removal, special character stripping,
whitespace normalization, stopword removal.

Applies food-domain-specific preprocessing that preserves compound terms
(e.g. "air fryer", "meal prep", "high protein") as single entities rather
than splitting them.

Author: Marlon J. Jones Jr.
"""

# TODO (Weeks 5-6): implement preprocess_all()
