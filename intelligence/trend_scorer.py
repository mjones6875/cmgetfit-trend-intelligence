"""
trend_scorer.py
----------------
Computes the composite trend score for each identified entity from four
weighted signals:

    score = (0.35 * velocity) + (0.30 * cross_platform)
          + (0.20 * engagement) + (0.15 * novelty)

- Velocity: week-over-week Google Trends search volume change (0-100 scale).
- Cross-platform momentum: count of distinct sources the entity appears in
  simultaneously — the most reliable noise filter.
- Engagement velocity: Reddit upvotes/comments relative to subreddit
  baseline, YouTube view growth rate.
- Novelty: inverse of historical frequency, favoring newly emerging terms
  over already-established ones.

Output: ranked list of entities with individual signal components and
composite score (0-100).

Author: Marlon J. Jones Jr.
"""

# TODO (Weeks 7-8): implement score_trends() and run the historical backtest
