from pathlib import Path
import xml.etree.ElementTree as ET

import pytest

from italian_champions_results.parser import read_results

DATA = Path(__file__).parent / "data"


@pytest.fixture
def results():
    return read_results(DATA / "results.xml")


def test_event(results):
    assert results.event.name == "Test Championship"
    assert results.event.start_date == "2026-09-12"


def test_categories_are_grouped(results):
    assert [c.name for c in results.categories] == ["M ELITE", "M B", "W ELITE", "W 10"]
    assert [len(c.entries) for c in results.categories] == [3, 3, 3, 2]


def test_athlete_and_valid_result(results):
    e = results.categories[0].entries[0]
    assert (e.athlete.family, e.athlete.given) == ("Rossi", "Mario")
    assert e.athlete.nationality == "ITA"
    assert e.athlete.club_id == "0098"
    assert e.athlete.club_name == "ASD PERCHÉ ORIENTEERING È BELLO"
    assert e.result.status == "OK"
    assert (e.result.position, e.result.time_seconds, e.result.time_behind) == (1, 1127, 0)


def test_athlete_without_id_and_club(results):
    a = results.categories[0].entries[1].athlete
    assert a.person_id is None
    assert a.nationality is None
    assert a.club_id is None and a.club_name is None


def test_foreign_athlete(results):
    hansen = results.categories[1].entries[0].athlete
    assert hansen.nationality == "AUT"


def test_non_ok_ignores_position_and_time(results):
    r = results.categories[0].entries[2].result
    assert r.status == "MissingPunch"
    assert r.position is None and r.time_seconds is None and r.time_behind is None


def test_malformed_xml():
    with pytest.raises(ET.ParseError):
        read_results(DATA / "malformed.xml")
