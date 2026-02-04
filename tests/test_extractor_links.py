from pathlib import Path

from email_extractor.extractor import extract_primary_links


def test_extract_primary_links_dedupes_preserves_order() -> None:
    sample = Path("samples/sample_email_1.html").read_text(encoding="utf-8")

    links = extract_primary_links(sample)

    assert links == [
        "https://example.com/releases",
        "https://example.com/dashboard",
    ]
