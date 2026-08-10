"""
clusterer.py
-------------
K-means clustering of the top-scored entities into coherent trend themes.

TF-IDF vectorizes the top 50 scored entities, runs K-means with k=5
(tunable, see config_template.yaml pipeline.k_clusters), and generates
cluster labels from the most distinctive terms per cluster. Clusters (not
individual entities) are passed to the brief generator, so e.g. "quinoa,
high protein grain, plant protein, grain bowl" becomes one labeled trend:
"High-Protein Plant Grains."

Author: Marlon J. Jones Jr.
"""

# TODO (Weeks 9-10): implement cluster_trends()
