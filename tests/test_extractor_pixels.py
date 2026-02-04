from pathlib import Path

from email_extractor.extractor import extract_tracking_pixels, parse_html_file


def test_extract_tracking_pixels_detects_1x1_and_hidden_style() -> None:
    sample = Path("samples/sample_email_1.html").read_text(encoding="utf-8")

    pixels = extract_tracking_pixels(sample)

    assert pixels == [
        "https://tracker.example.com/pixel-open?id=abc123",
        "https://tracker.example.com/hidden-style?id=xyz789",
    ]


def test_sample_email_2_has_no_pixels() -> None:
    result = parse_html_file(Path("samples/sample_email_2.html"))

    assert result.tracking_pixels == []
    assert len(result.tracking_pixels) == 0
