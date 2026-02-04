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

## Run

### A) Recommended (editable install)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pip install -e .
python -m email_extractor.cli --input samples --output output/extracted.csv
```

### B) Alternative (no install)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
PYTHONPATH=src python -m email_extractor.cli --input samples --output output/extracted.csv
```

Option B exists because the package source lives under `src/` and is not importable by default without installation.

This prints a short summary and writes the CSV file.

## Run tests

```bash
source .venv/bin/activate
pytest -q
```

## Output CSV format

The CLI writes one row per processed HTML file with these columns:

- `source_file`
- `primary_links` (semicolon-separated)
- `tracking_pixels` (semicolon-separated)
- `links_count`
- `pixels_count`

Header is always written. Inputs are processed deterministically (sorted `.html` files), and extraction order is stable with deduplication.
