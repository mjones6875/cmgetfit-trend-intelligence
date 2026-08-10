"""
run_pipeline.py
---------------
Main entry point for the CMgetFit Trend Intelligence pipeline.

Execution order:
1. Health check — verify all data sources are accessible
2. Ingestion — pull data from all sources
3. Processing — NLP extraction and scoring
4. Intelligence — trend scoring, clustering, brief generation
5. Output — push to Airtable, generate PDF report

Run this file on a schedule (Monday, Wednesday, Friday) or manually.

Usage: python run_pipeline.py
"""

import logging

from ingestion.health_check import run_health_check

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")


def run():
    logging.info("Starting CMgetFit Trend Intelligence Pipeline")

    # Step 1: Health check
    sources_ok = run_health_check()
    if not sources_ok:
        logging.warning("One or more sources failed health check. Running with available sources.")

    # Steps 2-5 will be implemented as modules are built (see build timeline in README)
    logging.info("Pipeline complete.")


if __name__ == "__main__":
    run()
