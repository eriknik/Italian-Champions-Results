from pathlib import Path

import pytest

from italian_champions_results.filters import filter_by_club, filter_winners
from italian_champions_results.parser import read_results

DATA = Path(__file__).parent / "data"


@pytest.fixture
def results():
    return read_results(DATA / "results.xml")


def families(results):
    return {c.name: [e.athlete.family for e in c.entries] for c in results.categories}


def test_club_filter_drops_empty_categories(results):
    filtered = filter_by_club(results, "0098")
    assert families(filtered) == {
        "M ELITE": ["Rossi", "Verdi"],
        "M B": ["Gialli"],
        "W ELITE": ["Grigi"],
        "W 10": ["Rosa"],
    }
    assert filtered.event == results.event


def test_club_filter_does_not_modify_original(results):
    filter_by_club(results, "0098")
    assert [len(c.entries) for c in results.categories] == [3, 3, 3, 2]


def test_winners_club_0098(results):
    # M B: the Austrian is ahead, so Gialli (first Italian) is the winner.
    # W ELITE: the winner is Neri (0982), so Grigi is not returned.
    # W 10: Rosa is tied for first place.
    assert families(filter_winners(results, "0098")) == {
        "M ELITE": ["Rossi"],
        "M B": ["Gialli"],
        "W 10": ["Rosa"],
    }


def test_winners_club_0982(results):
    # Hansen (AUT, club 0982) won M B overall but does not count;
    # Blu (0982) is third, not the best Italian.
    assert families(filter_winners(results, "0982")) == {
        "W ELITE": ["Neri"],
        "W 10": ["Viola"],
    }


def test_winners_unknown_club(results):
    assert filter_winners(results, "9999").categories == []


def test_winners_ignores_athletes_without_nationality(results):
    # Bianchi has no nationality: never a winner, even for a club-less lookup.
    winners = filter_winners(results, "0098")
    assert "Bianchi" not in [e.athlete.family for c in winners.categories for e in c.entries]


def test_winners_other_nationality(results):
    assert families(filter_winners(results, "0982", nationality="AUT")) == {"M B": ["Hansen"]}


def test_winners_do_not_modify_original(results):
    filter_winners(results, "0098")
    assert [len(c.entries) for c in results.categories] == [3, 3, 3, 2]
