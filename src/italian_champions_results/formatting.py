"""Small formatting helpers shared by the CLI and the CSV export."""
from typing import Optional


def format_time(seconds: Optional[int]) -> str:
    if seconds is None:
        return "-"
    h, rest = divmod(seconds, 3600)
    m, s = divmod(rest, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
