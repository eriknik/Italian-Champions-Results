"""Filters on parsed results."""
from dataclasses import replace

from .models import Category, EventResults

ITALY = "ITA"


def _keep_categories(results: EventResults, categories: list[Category]) -> EventResults:
    return replace(results, categories=categories)


def filter_by_club(results: EventResults, club_id: str) -> EventResults:
    """Keep only the club's athletes; drop categories left empty."""
    categories = []
    for cat in results.categories:
        entries = [e for e in cat.entries if e.athlete.club_id == club_id]
        if entries:
            categories.append(replace(cat, entries=entries))
    return _keep_categories(results, categories)


def filter_winners(
    results: EventResults, club_id: str, nationality: str = ITALY
) -> EventResults:
    """Keep only the club's category winners.

    The winner of a category is the best-placed finisher (status OK) with the
    given nationality: athletes of other nationalities are ignored, even if
    they finished ahead. The winner is chosen among all such athletes first
    and only then checked against the club, so a club athlete who is not the
    winner is never returned. Athletes tied for first place are all winners.
    Athletes with no nationality in the file are never considered winners.
    """
    categories = []
    for cat in results.categories:
        ranked = [
            (e.result.position, e)
            for e in cat.entries
            if e.result.position is not None and e.athlete.nationality == nationality
        ]
        if not ranked:
            continue
        best = min(pos for pos, _ in ranked)
        winners = [
            e for pos, e in ranked
            if pos == best and e.athlete.club_id == club_id
        ]
        if winners:
            categories.append(replace(cat, entries=winners))
    return _keep_categories(results, categories)
