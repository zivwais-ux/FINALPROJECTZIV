"""Web search for the latest market news, through Google News RSS (no API key).

The course brief asks the agent to search the web for news from the last 48
hours. Harbor & Vale is fictional, so the search covers a real market:
online retail in the United States, narrowed by the customer's preferred
category.

Google News serves search results as RSS without a key; `when:2d` limits them
to the last two days, and hl/gl/ceid pick English-language news for the US.
Articles older than 48 hours are dropped again here, in case the feed is
looser than the operator. Standard library and no crewai, so the web app can
use it too (the agent's tool wrapper lives in tools/briefing_tools.py).

A failed or slow search returns no articles and an error message, never an
exception: a briefing without news is still a briefing.
"""
from __future__ import annotations

import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import Any

FEED_URL = "https://news.google.com/rss/search"
WINDOW = timedelta(hours=48)
MAX_ARTICLES = 5
TIMEOUT_SECONDS = 8
MAX_BYTES = 1_000_000
CACHE_SECONDS = 15 * 60
LOCALE = {"hl": "en-US", "gl": "US", "ceid": "US:en"}

# Market news query per preferred category, in Google search syntax.
CATEGORY_QUERIES = {
    "Mobile": "smartphone (sale OR discount OR deal)",
    "Mobile Phone": "smartphone (sale OR discount OR deal)",
    "Laptop & Accessory": "(laptop OR electronics) (sale OR discount OR deal)",
    "Fashion": "fashion (ecommerce OR \"online shopping\" OR sale)",
    "Grocery": "(\"online grocery\" OR \"grocery delivery\")",
}
DEFAULT_QUERY = "(ecommerce OR \"online shopping\") (discount OR sale OR deal)"

_cache: dict[str, tuple[float, dict[str, Any]]] = {}
# Every article link any search returned in this process. Google issues a new
# link token for the same article on each request, so a briefing's guardrail
# checks links against all of them, not just one search's.
SEEN_URLS: set[str] = set()


# The US edition of Google News still lists some Indian outlets; leave them out.
EXCLUDE = "-India -Rs"


def news_query(category: str | None) -> str:
    return f"{CATEGORY_QUERIES.get(category or '', DEFAULT_QUERY)} {EXCLUDE}"


def parse_feed(xml_text: str, now: datetime, max_articles: int = MAX_ARTICLES) -> list[dict[str, str]]:
    """Articles from a Google News RSS document, newest first, within the 48-hour window."""
    articles = []
    for item in ET.fromstring(xml_text).iter("item"):
        try:
            published = parsedate_to_datetime(item.findtext("pubDate", ""))
        except (TypeError, ValueError):
            continue
        if published.tzinfo is None:
            published = published.replace(tzinfo=timezone.utc)
        if not timedelta(0) <= now - published <= WINDOW:
            continue
        source = item.find("source")
        outlet = source.text.strip() if source is not None and source.text else ""
        title = item.findtext("title", "").strip()
        # Google appends " - Outlet" to every title; the outlet is shown separately.
        if outlet and title.endswith(f" - {outlet}"):
            title = title[: -len(f" - {outlet}")]
        articles.append({"title": title, "url": item.findtext("link", "").strip(), "source": outlet,
                         "published": published.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
                         "_at": published})
    articles.sort(key=lambda a: a["_at"], reverse=True)
    return [{k: v for k, v in a.items() if k != "_at"} for a in articles[:max_articles]]


def search_recent_news(query: str, max_articles: int = MAX_ARTICLES) -> dict[str, Any]:
    """Articles Google News lists for query from the last 48 hours, newest first."""
    cached = _cache.get(query)
    if cached and time.time() - cached[0] < CACHE_SECONDS:
        return cached[1]
    url = f"{FEED_URL}?{urllib.parse.urlencode({'q': f'{query} when:2d', **LOCALE})}"
    result: dict[str, Any] = {"query": query, "window": "last 48 hours", "source": "Google News",
                              "articles": [], "error": None}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (churn-pipeline course project)"})
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
            body = response.read(MAX_BYTES).decode("utf-8", errors="replace")
        result["articles"] = parse_feed(body, datetime.now(timezone.utc), max_articles)
        SEEN_URLS.update(a["url"] for a in result["articles"])
    except (urllib.error.URLError, TimeoutError, ET.ParseError, ValueError, OSError) as e:
        result["error"] = f"news search unavailable: {e}"
    if result["error"] is None:
        _cache[query] = (time.time(), result)
    return result
