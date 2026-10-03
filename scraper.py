

import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AIWebScraperBot/1.0)"}


def fetch_page(page_num: int) -> str:
    """Download raw HTML for a given page number."""
    url = f"{BASE_URL}/page/{page_num}/"
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.text


def parse_page(html: str) -> list[dict]:
    """Extract quote, author, and tags from a page's HTML."""
    soup = BeautifulSoup(html, "html.parser")
    records = []

    for block in soup.select("div.quote"):
        text = block.select_one("span.text").get_text(strip=True).strip('"\u201c\u201d')
        author = block.select_one("small.author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in block.select("a.tag")]
        records.append({"text": text, "author": author, "tags": ", ".join(tags)})

    return records


def scrape_all(max_pages: int = 5, delay: float = 1.0) -> list[dict]:
    """
    Scrape multiple pages, stopping early if a page has no quotes
    (i.e. we've reached the end of the site). `delay` is a polite pause
    between requests so we don't hammer the server.
    """
    all_records = []
    for page_num in range(1, max_pages + 1):
        html = fetch_page(page_num)
        records = parse_page(html)
        if not records:
            break
        all_records.extend(records)
        time.sleep(delay)

    return all_records


if __name__ == "__main__":
    data = scrape_all(max_pages=3)
    print(f"Scraped {len(data)} quotes.")
    for item in data[:3]:
        print(item)
