import requests


def download_xml(url: str, timeout: int = 10) -> bytes:
    """Download the URL and return the content as bytes."""
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "italian-champions-results/0.1"},
    )
    response.raise_for_status()  # raises on 404, 500, etc.
    return response.content      # bytes: the XML declares its own encoding
