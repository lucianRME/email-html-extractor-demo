# email-html-extractor-poc

A small, public-safe Python PoC for an Upwork-style "Email HTML parsing & extraction" task. It only processes local sample HTML files (no IMAP, no credentials) and demonstrates extraction of:

- Primary links from `<a href="...">`
- Tracking pixels from `<img ...>` using simple heuristics
- CSV export of per-file results

## Tech stack

- Python 3.11+
- beautifulsoup4
- lxml
- pytest

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pip install -e .
```

## Run the CLI

From the repository root:

```bash
python -m email_extractor.cli --input samples --output output/extracted.csv
```

This prints a short summary and writes the CSV file.

## Run tests

```bash
pytest
```

## Output CSV format

The CLI writes one row per processed HTML file with these columns:

- `source_file`
- `primary_links` (semicolon-separated)
- `tracking_pixels` (semicolon-separated)
- `links_count`
- `pixels_count`

Header is always written. Inputs are processed deterministically (sorted `.html` files), and extraction order is stable with deduplication.
