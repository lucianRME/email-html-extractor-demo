"""CLI for local email HTML extraction demo."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .extractor import gather_html_files, parse_html_file, write_results_csv


def build_parser() -> argparse.ArgumentParser:
    """Build and return command-line argument parser."""
    parser = argparse.ArgumentParser(description="Extract links and tracking pixels from HTML files")
    parser.add_argument("--input", required=True, help="Input HTML file or directory")
    parser.add_argument("--output", default="output/extracted.csv", help="Output CSV path")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI and return process exit code."""
    args = build_parser().parse_args(argv)

    input_path = Path(args.input)
    output_path = Path(args.output)

    html_files = gather_html_files(input_path)
    results = [parse_html_file(path) for path in html_files]
    write_results_csv(results, output_path)

    total_links = sum(len(item.primary_links) for item in results)
    total_pixels = sum(len(item.tracking_pixels) for item in results)
    print(f"Processed {len(results)} files, total links: {total_links}, total pixels: {total_pixels}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
