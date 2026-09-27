"""Export parsed results to CSV."""
import csv
from typing import TextIO, Union

from .formatting import format_time
from .models import EventResults

FIELDNAMES = [
    "event_name",
    "event_date",
    "category",
    "family",
    "given",
    "person_id",
    "nationality",
    "club_id",
    "club_name",
    "bib",
    "status",
    "position",
    "time_seconds",
    "time",
    "time_behind",
    "start_time",
    "finish_time",
]


def _rows(results: EventResults):
    for cat in results.categories:
        for e in cat.entries:
            a, r = e.athlete, e.result
            yield {
                "event_name": results.event.name,
                "event_date": results.event.start_date,
                "category": cat.name,
                "family": a.family,
                "given": a.given,
                "person_id": a.person_id,
                "nationality": a.nationality,
                "club_id": a.club_id,
                "club_name": a.club_name,
                "bib": r.bib,
                "status": r.status,
                "position": r.position,
                "time_seconds": r.time_seconds,
                "time": format_time(r.time_seconds),
                "time_behind": r.time_behind,
                "start_time": r.start_time,
                "finish_time": r.finish_time,
            }


def write_csv(results: EventResults, file: Union[str, TextIO]) -> None:
    """Write one row per athlete, with a header, to a path or an open text file."""
    if isinstance(file, str):
        with open(file, "w", newline="", encoding="utf-8") as f:
            _write(results, f)
    else:
        _write(results, file)


def _write(results: EventResults, f: TextIO) -> None:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
    writer.writeheader()
    for row in _rows(results):
        writer.writerow(row)
