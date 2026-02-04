import csv
from pathlib import Path

from email_extractor.cli import main


def test_cli_smoke_writes_expected_csv(tmp_path: Path) -> None:
    output_csv = tmp_path / "extracted.csv"

    exit_code = main(["--input", "samples", "--output", str(output_csv)])

    assert exit_code == 0
    assert output_csv.exists()

    with output_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    assert reader.fieldnames == [
        "source_file",
        "primary_links",
        "tracking_pixels",
        "links_count",
        "pixels_count",
    ]
    assert len(rows) == 2
