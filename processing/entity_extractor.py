"""
entity_extractor.py
--------------------
Named entity recognition using spaCy (en_core_web_lg).

Extracts FOOD, PRODUCT, and relevant noun phrases against a food entity
whitelist (~500 common food terms) and blacklist of known false positives
(e.g. "dates" as calendar dates, "lettuce" as slang). Merges singular and
plural forms of the same entity (chickpea / chickpeas) during post-processing.

Author: Marlon J. Jones Jr.
"""

# TODO (Weeks 5-6): implement extract_entities() and build the food whitelist/blacklist
