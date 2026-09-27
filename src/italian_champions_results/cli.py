import argparse
import sys
import xml.etree.ElementTree as ET
from typing import Optional

import requests

from .download import download_xml
from .models import EventResults
from .csv_export import write_csv
from .filters import filter_by_club, filter_winners
from .formatting import format_time
from .parser import parse_results, read_results

URL_BASE = "https://www.fiso.it/_files/risultati_gara_files/imported/{}.xml"


def print_results(results: EventResults) -> None:
    ev = results.event
    print(f"{ev.name} - {ev.start_date or 'date unknown'}")
    for cat in results.categories:
        print(f"\n{cat.name}")
        for e in cat.entries:
            a, r = e.athlete, e.result
            pos = r.position if r.position is not None else "-"
            print(
                f"  {pos!s:>3}  {a.family + ' ' + a.given:<28} "
                f"{a.club_name or '-':<35} {format_time(r.time_seconds):>8}  {r.status}"
            )


def main(argv: Optional[list[str]] = None) -> None:
    ap = argparse.ArgumentParser(
        description="Download results from the Italian Orienteering Federation "
                    "website and parse the XML file (IOF 3.0 format)"
    )
    groups = ap.add_mutually_exclusive_group(required=True)
    groups.add_argument("--id", help="event ID (e.g. 1234)")
    groups.add_argument("--file", help="parse a local XML file")
    ap.add_argument("--clubid", required=True, help="club ID (e.g. 0098)")
    ap.add_argument(
        "--csv",
        metavar="PATH",
        help="also export the filtered results to a CSV file (with header)",
    )
    ap.add_argument(
        "--winners",
        action="store_true",
        help="only show the club's category winners "
             "(the best-placed Italian athlete of each category)",
    )
    args = ap.parse_args(argv)

    try:
        if args.file:
            results = read_results(args.file)
        else:
            results = parse_results(download_xml(URL_BASE.format(args.id)))
    except FileNotFoundError:
        print("File not found", file=sys.stderr)
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Download error: {e}", file=sys.stderr)
        sys.exit(1)
    except ET.ParseError as e:
        print(f"Invalid XML: {e}", file=sys.stderr)
        sys.exit(1)

    if args.winners:
        filtered = filter_winners(results, args.clubid)
    else:
        filtered = filter_by_club(results, args.clubid)
    if not filtered.categories:
        what = "winners" if args.winners else "results"
        print(f"{results.event.name}: no {what} for club {args.clubid}")
        return
    print_results(filtered)
    if args.csv:
        write_csv(filtered, args.csv)
        print(f"\nCSV written to {args.csv}")


if __name__ == "__main__":
    main()
