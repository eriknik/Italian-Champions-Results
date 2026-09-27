import csv
from io import StringIO
from pathlib import Path

from italian_champions_results.csv_export import write_csv
from italian_champions_results.filters import filter_by_club, filter_winners
from italian_champions_results.parser import read_results

DATA = Path(__file__).parent / "data"


def test_header_and_row_count():
    results = read_results(DATA / "results.xml")
    buf = StringIO()
    write_csv(results, buf)
    rows = list(csv.DictReader(StringIO(buf.getvalue())))
    assert list(rows[0].keys())[:6] == [
        "event_name", "event_date", "category", "family", "given", "person_id",
    ]
    assert len(rows) == sum(len(c.entries) for c in results.categories)


def test_row_content_matches_the_model():
    results = read_results(DATA / "results.xml")
    buf = StringIO()
    write_csv(results, buf)
    row = next(csv.DictReader(StringIO(buf.getvalue())))
    assert row["event_name"] == "Test Championship"
    assert row["event_date"] == "2026-09-12"
    assert row["category"] == "M ELITE"
    assert row["family"] == "Rossi"
    assert row["nationality"] == "ITA"
    assert row["club_id"] == "0098"
    assert row["position"] == "1"
    assert row["time_seconds"] == "1127"
    assert row["time"] == "18:47"


def test_missing_values_are_empty_strings():
    results = read_results(DATA / "results.xml")
    buf = StringIO()
    write_csv(results, buf)
    rows = list(csv.DictReader(StringIO(buf.getvalue())))
    bianchi = next(r for r in rows if r["family"] == "Bianchi")
    assert bianchi["nationality"] == "" and bianchi["club_id"] == ""


def test_non_ok_status_has_empty_position_and_time():
    results = read_results(DATA / "results.xml")
    buf = StringIO()
    write_csv(results, buf)
    rows = list(csv.DictReader(StringIO(buf.getvalue())))
    verdi = next(r for r in rows if r["family"] == "Verdi")
    assert verdi["status"] == "MissingPunch"
    assert verdi["position"] == "" and verdi["time_seconds"] == ""
    assert verdi["time"] == "-"


def test_export_reflects_filters():
    results = read_results(DATA / "results.xml")
    buf = StringIO()
    write_csv(filter_by_club(results, "0098"), buf)
    rows = list(csv.DictReader(StringIO(buf.getvalue())))
    assert {r["family"] for r in rows} == {"Rossi", "Verdi", "Gialli", "Grigi", "Rosa"}

    buf2 = StringIO()
    write_csv(filter_winners(results, "0098"), buf2)
    rows2 = list(csv.DictReader(StringIO(buf2.getvalue())))
    assert {r["family"] for r in rows2} == {"Rossi", "Gialli", "Rosa"}


def test_write_to_path(tmp_path):
    results = read_results(DATA / "results.xml")
    out = tmp_path / "out.csv"
    write_csv(results, str(out))
    text = out.read_text(encoding="utf-8")
    assert text.startswith("event_name,")
    assert "Rossi" in text
