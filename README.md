# Italian Champions Results

Downloads the results of an orienteering event from the Italian Orienteering
Federation website (IOF XML 3.0 format) and prints the event name and date and,
grouped by category, each athlete's details and result. Results can be filtered
by club (`--clubid`); categories with no athletes from the club are not shown.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Usage

```bash
italian-champions-results --id 202613 --clubid 0098        # download event 202613
italian-champions-results --file 202613.xml --clubid 0098  # parse a local file
python -m italian_champions_results --id 202613 --clubid 0098
italian-champions-results --file 202613.xml --clubid 0098 --winners   # only category winners
italian-champions-results --file 202613.xml --clubid 0098 --csv out.csv  # also export to CSV
```

### CSV export (`--csv PATH`)

Writes one row per athlete to `PATH`, with a header, reflecting whatever the current
filters (`--clubid`, `--winners`) selected. Columns: `event_name`, `event_date`,
`category`, `family`, `given`, `person_id`, `nationality`, `club_id`, `club_name`,
`bib`, `status`, `position`, `time_seconds`, `time` (`h:mm:ss`), `time_behind`,
`start_time`, `finish_time`. Missing values are empty. Fields set only for status `OK`
(`position`, `time_seconds`, `time_behind`) are empty for other statuses. Nothing is
written if the filters match no athlete.

### Winners (`--winners`)

Shows only the club's category winners. The winner of a category is the best-placed
**Italian** finisher: athletes of other nationalities are ignored even if they finished
ahead. The winner is chosen among all Italians first, then checked against the club, so
a club athlete who is not the winner is never shown. Athletes tied for first are all
winners. The position printed is the one in the file (overall), so an Italian winner can
show a position greater than 1 if foreigners finished ahead.

## Tests and type checking

```bash
pytest
mypy src
```

## Project layout

```
src/italian_champions_results/
├── models.py     # dataclasses: Event, Athlete, Result, Entry, Category, EventResults
├── parser.py     # parse_results(), read_results()
├── filters.py    # filter_by_club(), filter_winners()
├── csv_export.py # write_csv()
├── formatting.py # format_time()
├── download.py   # download_xml()
└── cli.py        # --id / --file / --clubid
```

## Notes on the data

- Position, time and time behind are set only when the status is `OK`. For the other
  statuses (`MissingPunch`, `DidNotStart`, `DidNotFinish`, `OverTime`) the file contains
  meaningless values, so they are ignored.
- Some athletes have no federation ID, nationality or club: those fields are `None`.
  An athlete with no nationality is never counted as Italian when finding winners.
- Nationality is that of the athlete (`Person/Nationality`), not the club's country:
  a foreign athlete can run for an Italian club.
- Split times (`SplitTime`) are not read.
- The club ID is compared as a string, so use `0098`, not `98`.

## Customization

- Site URL: `URL_BASE` in `src/italian_champions_results/cli.py`
- Timeout and HTTP headers: `src/italian_champions_results/download.py`
- If the XML comes from an untrusted source, replace `xml.etree.ElementTree` with
  `defusedxml.ElementTree` (`pip install defusedxml`).
