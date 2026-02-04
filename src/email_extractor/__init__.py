"""Email HTML extractor PoC package."""

from .extractor import (
    ExtractionResult,
    extract_primary_links,
    extract_tracking_pixels,
    parse_html_file,
    write_results_csv,
)

__all__ = [
    "ExtractionResult",
    "extract_primary_links",
    "extract_tracking_pixels",
    "parse_html_file",
    "write_results_csv",
]
