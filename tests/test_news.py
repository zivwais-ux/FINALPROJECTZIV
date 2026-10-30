"""Google News search, tested without the network."""
import io
from datetime import datetime, timezone

import churn_pipeline.news as news

NOW = datetime(2026, 10, 30, 16, 0, tzinfo=timezone.utc)
FEED = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>search</title>
<item><title>Big phone sale this week - Example Times</title><link>https://news.google.com/a1</link>
  <pubDate>Fri, 30 Oct 2026 10:00:00 GMT</pubDate><source url="https://example.com">Example Times</source></item>
<item><title>Older story - Old Daily</title><link>https://news.google.com/a2</link>
  <pubDate>Mon, 26 Oct 2026 10:00:00 GMT</pubDate><source url="https://old.example">Old Daily</source></item>
<item><title>Newest discount war - Daily Mint</title><link>https://news.google.com/a3</link>
  <pubDate>Fri, 30 Oct 2026 15:30:00 GMT</pubDate><source url="https://mint.example">Daily Mint</source></item>
</channel></rss>"""


def test_parse_feed_keeps_the_last_48_hours_newest_first():
    articles = news.parse_feed(FEED, NOW)
    assert [a["title"] for a in articles] == ["Newest discount war", "Big phone sale this week"]
    assert articles[0] == {"title": "Newest discount war", "url": "https://news.google.com/a3",
                           "source": "Daily Mint", "published": "2026-10-30 15:30 UTC"}


def test_query_follows_the_category():
    assert news.news_query("Mobile Phone").startswith("smartphone")
    assert news.news_query("Grocery").startswith('("quick commerce"')
    assert news.news_query(None) == news.DEFAULT_QUERY


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def test_search_asks_google_news_for_two_days_in_india(monkeypatch):
    seen = []

    def fake_urlopen(req, timeout):
        seen.append(req.full_url)
        return FakeResponse(FEED.encode())

    monkeypatch.setattr(news.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(news, "_cache", {})
    result = news.search_recent_news("smartphone sale India")
    assert result["error"] is None and result["source"] == "Google News"
    assert "when%3A2d" in seen[0] and "gl=IN" in seen[0] and "hl=en-IN" in seen[0]
    news.search_recent_news("smartphone sale India")
    assert len(seen) == 1  # cached


def test_unreachable_news_returns_an_error_not_an_exception(monkeypatch):
    def refuse(req, timeout):
        raise news.urllib.error.URLError("blocked")

    monkeypatch.setattr(news.urllib.request, "urlopen", refuse)
    monkeypatch.setattr(news, "_cache", {})
    result = news.search_recent_news("anything")
    assert result["articles"] == [] and "unavailable" in result["error"]
