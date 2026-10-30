"""Web search for the latest market news, through GDELT (no API key).

The course brief asks the agent to search the web for news from the last 48
hours. Harbor & Vale is fictional, so the search covers its real market:
online retail in India, narrowed by the customer's preferred category.

GDELT's DOC 2.0 API (https://api.gdeltproject.org/api/v2/doc/doc) is free and
needs no key. Standard library and no crewai, so the web app can use it too (the agent's
tool wrapper lives in tools/briefing_tools.py). A failed
or slow search returns no articles and an error message, never an exception:
a briefing without news is still a briefing.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
TIMESPAN = "48h"
MAX_ARTICLES = 5
TIMEOUT_SECONDS = 8
CACHE_SECONDS = 15 * 60

# Market news query per preferred category. Space means AND in GDELT; the
# filters keep English-language sources from India.
_FILTERS = "sourcecountry:india sourcelang:english"
CATEGORY_QUERIES = {
    "Mobile": "(smartphone OR mobile) (sale OR discount OR offer)",
    "Mobile Phone": "(smartphone OR mobile) (sale OR discount OR offer)",
    "Laptop & Accessory": "(laptop OR electronics) (sale OR discount OR offer)",
    "Fashion": "fashion (ecommerce OR \"online shopping\" OR sale)",
    "Grocery": "(\"quick commerce\" OR grocery) delivery",
}
DEFAULT_QUERY = "(ecommerce OR \"online shopping\") (discount OR sale OR offer)"

_cache: dict[str, tuple[float, dict[str, Any]]] = {}


def news_query(category: str | None) -> str:
    return f"{CATEGORY_QUERIES.get(category or '', DEFAULT_QUERY)} {_FILTERS}"


def _published(seendate: str) -> str:
    """GDELT's 20261030T141500Z as 2026-10-30 14:15 UTC."""
    try:
        return time.strftime("%Y-%m-%d %H:%M UTC", time.strptime(seendate, "%Y%m%dT%H%M%SZ"))
    except (TypeError, ValueError):
        return seendate or ""


def search_recent_news(query: str, max_articles: int = MAX_ARTICLES) -> dict[str, Any]:
    """Articles GDELT saw in the last 48 hours for query, newest first."""
    cached = _cache.get(query)
    if cached and time.time() - cached[0] < CACHE_SECONDS:
        return cached[1]
    params = {"query": query, "mode": "artlist", "format": "json", "timespan": TIMESPAN,
              "maxrecords": str(max_articles), "sort": "datedesc"}
    url = f"{GDELT_URL}?{urllib.parse.urlencode(params)}"
    result: dict[str, Any] = {"query": query, "timespan": TIMESPAN, "source": "GDELT DOC 2.0",
                              "articles": [], "error": None}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "churn-pipeline-course-project"})
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
            text = response.read().decode("utf-8", errors="replace")
        # GDELT answers a malformed query with plain text instead of JSON.
        data = json.loads(text) if text.lstrip().startswith("{") else {}
        if not data and text.strip():
            result["error"] = f"GDELT did not return results: {text.strip()[:160]}"
        for a in data.get("articles", [])[:max_articles]:
            result["articles"].append({"title": a.get("title", "").strip(), "url": a.get("url", ""),
                                       "domain": a.get("domain", ""),
                                       "published": _published(a.get("seendate", ""))})
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as e:
        result["error"] = f"news search unavailable: {e}"
    if result["error"] is None:
        _cache[query] = (time.time(), result)
    return result

