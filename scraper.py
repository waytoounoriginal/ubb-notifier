from __future__ import annotations

import re
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from article import Article


class Scraper:
    BASE_URL = "https://www.cs.ubbcluj.ro/"
    _POST_ID_PATTERN = re.compile(r"post-\d+")

    def __init__(self, url: str | None = None) -> None:
        self.url = url or self.BASE_URL

    def scrape(self) -> list[Article]:
        html = self._fetch_html()
        soup = BeautifulSoup(html, "html.parser")
        return self._parse_articles(soup)

    def _fetch_html(self) -> str:
        request = Request(
            self.url,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; UBBNotifierScraper/1.0)",
            },
        )
        with urlopen(request) as response:
            return response.read().decode("utf-8", errors="replace")

    def _parse_articles(self, soup: BeautifulSoup) -> list[Article]:
        articles: list[Article] = []

        for post_div in soup.select('div[id^="post-"]'):
            post_id = post_div.get("id", "")
            if not self._POST_ID_PATTERN.fullmatch(post_id):
                continue

            title_link = post_div.select_one("h2.title > a[title]")
            overview_div = post_div.select_one("div.entry")

            if title_link is None or overview_div is None:
                continue

            title = title_link.get_text(" ", strip=True)
            overview = overview_div.get_text(" ", strip=True)

            if not title:
                continue

            articles.append(Article(title=title, overview=overview))

        return articles
