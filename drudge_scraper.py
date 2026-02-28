import csv
import datetime
import requests
from bs4 import BeautifulSoup

URL = "https://www.drudgereport.com"

# Minimum character length to filter out short navigation/icon links
MIN_HEADLINE_LENGTH = 10


def get_headlines(url=URL):
    """Fetch headline links from drudgereport.com and return them as a list of strings."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Failed to fetch headlines from {url}: {exc}") from exc

    soup = BeautifulSoup(response.text, "html.parser")

    headlines = []
    for tag in soup.find_all("a"):
        text = tag.get_text(strip=True)
        if len(text) >= MIN_HEADLINE_LENGTH:
            headlines.append(text)

    return headlines


def save_to_csv(headlines, filename="drudge_headlines.csv", append=False):
    """Write headlines to a CSV file with the UTC date/time they were pulled.

    Args:
        headlines: List of headline strings to write.
        filename:  Path of the output CSV file (default: drudge_headlines.csv).
        append:    When True, append rows to an existing file instead of
                   overwriting it (default: False).
    """
    pulled_at = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )
    mode = "a" if append else "w"
    write_header = not append
    with open(filename, mode, newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if write_header:
            writer.writerow(["date_pulled", "headline"])
        for headline in headlines:
            writer.writerow([pulled_at, headline])
    print(f"Saved {len(headlines)} headlines to '{filename}'")


if __name__ == "__main__":
    headlines = get_headlines()
    save_to_csv(headlines)
