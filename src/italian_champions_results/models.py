from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Event:
    name: str
    start_date: Optional[str]     # e.g. "2026-09-12"


@dataclass
class Athlete:
    person_id: Optional[str]      # federation ID (may be missing)
    family: str
    given: str
    nationality: Optional[str]    # IOC code of the athlete, e.g. "ITA" (may be missing)
    club_id: Optional[str]        # may be missing
    club_name: Optional[str]


@dataclass
class Result:
    bib: Optional[str]
    start_time: Optional[str]     # ISO 8601, e.g. 2026-09-12T14:30:13.000+02:00
    finish_time: Optional[str]
    status: str                   # OK, MissingPunch, DidNotStart, DidNotFinish, ...
    # Set only when status == "OK", otherwise None
    time_seconds: Optional[int] = None
    time_behind: Optional[int] = None
    position: Optional[int] = None


@dataclass
class Entry:
    athlete: Athlete
    result: Result


@dataclass
class Category:
    name: str                     # e.g. "M ELITE"
    entries: list[Entry] = field(default_factory=list)


@dataclass
class EventResults:
    event: Event
    categories: list[Category] = field(default_factory=list)
