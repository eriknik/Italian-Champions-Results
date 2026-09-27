"""Parse an IOF XML 3.0 ResultList: event, categories, athletes and results."""
import xml.etree.ElementTree as ET
from typing import Optional, Union

from .models import Athlete, Category, Entry, Event, EventResults, Result

NS = {"i": "http://www.orienteering.org/datastandard/3.0"}


def _text(el: Optional[ET.Element], path: str) -> Optional[str]:
    """Stripped text of a child element, or None if missing or empty."""
    if el is None:
        return None
    value = el.findtext(path, namespaces=NS)
    value = value.strip() if value else ""
    return value or None


def _attr(el: Optional[ET.Element], path: str, name: str) -> Optional[str]:
    """Attribute of a child element, or None if the element or attribute is missing."""
    if el is None:
        return None
    child = el.find(path, NS)
    value = child.get(name) if child is not None else None
    return value.strip() or None if value else None


def _int(value: Optional[str]) -> Optional[int]:
    return int(value) if value is not None else None


def _parse_event(root: ET.Element) -> Event:
    ev = root.find("i:Event", NS)
    return Event(
        name=_text(ev, "i:Name") or "",
        start_date=_text(ev, "i:StartTime/i:Date"),
    )


def _parse_athlete(person_result: ET.Element) -> Athlete:
    person = person_result.find("i:Person", NS)
    org = person_result.find("i:Organisation", NS)  # missing for some athletes
    return Athlete(
        person_id=_text(person, "i:Id"),
        family=_text(person, "i:Name/i:Family") or "",
        given=_text(person, "i:Name/i:Given") or "",
        nationality=_attr(person, "i:Nationality", "code"),
        club_id=_text(org, "i:Id"),
        club_name=_text(org, "i:Name"),
    )


def _parse_result(person_result: ET.Element) -> Result:
    res = person_result.find("i:Result", NS)
    status = _text(res, "i:Status") or "Unknown"
    result = Result(
        bib=_text(res, "i:BibNumber"),
        start_time=_text(res, "i:StartTime"),
        finish_time=_text(res, "i:FinishTime"),
        status=status,
    )
    # For athletes without a valid result (disqualified, retired, did not
    # start) the file holds meaningless values, so they are ignored.
    if status == "OK":
        result.time_seconds = _int(_text(res, "i:Time"))
        result.time_behind = _int(_text(res, "i:TimeBehind"))
        result.position = _int(_text(res, "i:Position"))
    return result


def parse_results(data: Union[bytes, str]) -> EventResults:
    """Parse IOF XML 3.0 content (bytes or str) into event and per-category results."""
    root = ET.fromstring(data)
    categories = []
    for cls in root.findall("i:ClassResult", NS):
        entries = [
            Entry(_parse_athlete(pr), _parse_result(pr))
            for pr in cls.findall("i:PersonResult", NS)
        ]
        categories.append(Category(_text(cls, "i:Class/i:Name") or "", entries))
    return EventResults(_parse_event(root), categories)


def read_results(path: str) -> EventResults:
    """Parse a local XML file."""
    with open(path, "rb") as f:
        return parse_results(f.read())

