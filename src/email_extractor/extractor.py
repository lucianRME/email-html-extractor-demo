"""Core extraction logic for links and tracking pixels."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv

from bs4 import BeautifulSoup, Tag

from .utils import dedupe_preserve_order


@dataclass(frozen=True)
class ExtractionResult:
    """Result for a single source HTML file."""

    source_file: str
    primary_links: list[str]
    tracking_pixels: list[str]


def extract_primary_links(html: str) -> list[str]:
    """Extract all non-empty href values from anchor tags, preserving order."""
    soup = BeautifulSoup(html, "lxml")
    links: list[str] = []
    for anchor in soup.find_all("a"):
        href = anchor.get("href")
        if href is None:
            continue
        normalized = str(href).strip()
        if normalized:
            links.append(normalized)
    return dedupe_preserve_order(links)


def _parse_int(value: object) -> int | None:
    """Parse integer-like width/height values from HTML attributes."""
    if value is None:
        return None
    text = str(value).strip().lower().replace("px", "")
    if not text:
        return None
    if text.isdigit():
        return int(text)
    return None


def _is_tracking_pixel(image: Tag) -> bool:
    """Apply simple heuristics to classify whether an image is a tracking pixel."""
    width = _parse_int(image.get("width"))
    height = _parse_int(image.get("height"))
    if width == 1 and height == 1:
        return True
    if width == 0 or height == 0:
        return True

    style = str(image.get("style", "")).lower().replace(" ", "")
    if any(flag in style for flag in ("display:none", "visibility:hidden", "opacity:0")):
        return True

    if image.has_attr("hidden"):
        return True

    return False


def extract_tracking_pixels(html: str) -> list[str]:
    """Extract tracking pixel image sources based on heuristic matching."""
    soup = BeautifulSoup(html, "lxml")
    pixels: list[str] = []
    for image in soup.find_all("img"):
        src = image.get("src")
        if src is None:
            continue
        normalized = str(src).strip()
        if not normalized:
            continue
        if _is_tracking_pixel(image):
            pixels.append(normalized)
    return dedupe_preserve_order(pixels)


def parse_html_file(path: Path) -> ExtractionResult:
    """Parse one HTML file and return extracted links and tracking pixels."""
    html = path.read_text(encoding="utf-8")
    links = extract_primary_links(html)
    pixels = extract_tracking_pixels(html)
    return ExtractionResult(
        source_file=path.name,
        primary_links=links,
        tracking_pixels=pixels,
    )


def gather_html_files(input_path: Path) -> list[Path]:
    """Resolve input file(s) into a sorted list of HTML file paths."""
    if input_path.is_file():
        if input_path.suffix.lower() != ".html":
            return []
        return [input_path]

    if input_path.is_dir():
        return sorted(p for p in input_path.glob("*.html") if p.is_file())

    return []


def write_results_csv(results: list[ExtractionResult], output_path: Path) -> None:
    """Write extraction results to CSV with a stable schema and ordering."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "source_file",
                "primary_links",
                "tracking_pixels",
                "links_count",
                "pixels_count",
            ],
        )
        writer.writeheader()
        for result in results:
            writer.writerow(
                {
                    "source_file": result.source_file,
                    "primary_links": ";".join(result.primary_links),
                    "tracking_pixels": ";".join(result.tracking_pixels),
                    "links_count": len(result.primary_links),
                    "pixels_count": len(result.tracking_pixels),
                }
            )
