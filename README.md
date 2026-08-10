# CMgetFit Trend Intelligence

A multi-source NLP pipeline that identifies emerging food and wellness trends
2-4 weeks before mainstream peak engagement.

## What It Does

Ingests data from Google Trends, Reddit, YouTube, and News API on a weekly
schedule. Applies Named Entity Recognition, TF-IDF analysis, and sentiment
classification to extract food trend signals. Scores trends using a composite
algorithm combining search velocity, cross-platform momentum, engagement
velocity, and novelty. Clusters related trends using K-means and generates a
weekly content brief via the Anthropic Claude API, delivered to Airtable and
as a PDF report.

## Tech Stack

Python 3.11 | spaCy | HuggingFace Transformers | scikit-learn |
Anthropic Claude API | YouTube Data API v3 | PRAW | pytrends |
SQLite | Airtable | reportlab

## Academic Context

M.S. Artificial Intelligence Capstone — Kennesaw State University, December 2026

**Title:** Multi-Source NLP Pipeline for Emerging Trend Detection in the Food
and Wellness Domain

**Problem Statement:** Food and wellness content creators make content
decisions reactively, often posting about trends after peak engagement has
passed. This work proposes and evaluates an automated trend intelligence
system that identifies emerging topics 2-4 weeks before mainstream saturation
using multi-source NLP analysis.

**Validation Methodology:** Historical backtest on 6 months of Google Trends
and Reddit data, measuring precision and recall of trend predictions against
verified viral content performance in subsequent weeks.

## Repository Structure

```
├── config/config_template.yaml   # committed — placeholder values only
├── ingestion/                    # one module per data source
├── processing/                   # NLP: text cleanup, NER, TF-IDF, sentiment
├── intelligence/                 # trend scoring, clustering, brief generation
├── output/                       # Airtable push, PDF report, velocity alerts
├── data/                         # local only — contents gitignored
├── notebooks/                    # exploration and validation notebooks
├── tests/                        # pytest unit tests
└── run_pipeline.py               # main entry point
```

## Setup

1. Clone the repo
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Download the spaCy model: `python -m spacy download en_core_web_lg`
6. Copy `config/config_template.yaml`'s structure into a `.env` file in the
   project root and fill in your own API keys (see below)
7. Run: `python run_pipeline.py`

## Security

- Real API keys live only in a local `.env` file at the project root, which
  is git-ignored and must never be committed.
- `config/config_template.yaml` is the committed reference — placeholder
  values only.
- No raw usernames, post IDs, or other personally identifiable data from
  Reddit/YouTube/News sources are stored — only aggregated entity
  frequencies and trend scores.
- Every ingestion module implements exponential backoff on rate-limit
  responses.

## Status

Pre-build / early scaffold (Weeks 1-2 of a 16-week build). Ingestion,
processing, and intelligence modules are structural stubs pending
implementation.
