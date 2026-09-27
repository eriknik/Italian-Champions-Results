import csv
from pathlib import Path

from italian_champions_results import cli

DATA = Path(__file__).parent / "data"


def test_csv_flag_writes_file_and_reports_it(tmp_path, capsys):
    out = tmp_path / "results.csv"
    cli.main([
        "--file", str(DATA / "results.xml"),
        "--clubid", "0098",
        "--csv", str(out),
    ])
    console = capsys.readouterr().out
    assert f"CSV written to {out}" in console
    assert out.exists()

    with open(out, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert {r["family"] for r in rows} == {"Rossi", "Verdi", "Gialli", "Grigi", "Rosa"}


def test_csv_flag_combined_with_winners(tmp_path, capsys):
    out = tmp_path / "winners.csv"
    cli.main([
        "--file", str(DATA / "results.xml"),
        "--clubid", "0098",
        "--winners",
        "--csv", str(out),
    ])
    with open(out, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert {r["family"] for r in rows} == {"Rossi", "Gialli", "Rosa"}


def test_no_csv_written_without_flag(tmp_path, capsys):
    cli.main(["--file", str(DATA / "results.xml"), "--clubid", "0098"])
    assert "CSV written to" not in capsys.readouterr().out
    assert list(tmp_path.iterdir()) == []


def test_csv_not_written_when_no_matches(tmp_path, capsys):
    out = tmp_path / "empty.csv"
    cli.main([
        "--file", str(DATA / "results.xml"),
        "--clubid", "9999",
        "--csv", str(out),
    ])
    assert not out.exists()
    assert "no results for club 9999" in capsys.readouterr().out
