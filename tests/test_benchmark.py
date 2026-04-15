import os
import time
import unittest

from bs4 import BeautifulSoup

from scraper import Scraper


def _build_sample_html(post_count: int) -> str:
    posts = []
    for i in range(1, post_count + 1):
        posts.append(
            f"""
            <div id=\"post-{i}\">
                <h2 class=\"title\"><a title=\"Article {i}\" href=\"#\">Article {i}</a></h2>
                <div class=\"entry\">Overview text for article {i}.</div>
            </div>
            """
        )

    return "<html><body>" + "".join(posts) + "</body></html>"


class TestScraperBenchmark(unittest.TestCase):
    def test_parse_articles_average_time(self) -> None:
        runs = int(os.getenv("BENCHMARK_PARSE_RUNS", "40"))
        threshold = float(os.getenv("BENCHMARK_PARSE_AVG_THRESHOLD_SEC", "0.035"))

        scraper = Scraper()
        soup = BeautifulSoup(_build_sample_html(post_count=200), "html.parser")

        timings = []
        parsed_articles = []

        for _ in range(runs):
            start = time.perf_counter()
            parsed_articles = scraper._parse_articles(soup)
            timings.append(time.perf_counter() - start)

        average = sum(timings) / len(timings)

        self.assertEqual(len(parsed_articles), 200)
        self.assertLess(
            average,
            threshold,
            msg=f"Average parse time {average:.6f}s exceeded threshold {threshold:.6f}s",
        )

    def test_scrape_average_time_without_network(self) -> None:
        runs = int(os.getenv("BENCHMARK_SCRAPE_RUNS", "30"))
        threshold = float(os.getenv("BENCHMARK_SCRAPE_AVG_THRESHOLD_SEC", "0.045"))

        html = _build_sample_html(post_count=120)
        scraper = Scraper()
        scraper._fetch_html = lambda: html

        timings = []
        parsed_articles = []

        for _ in range(runs):
            start = time.perf_counter()
            parsed_articles = scraper.scrape()
            timings.append(time.perf_counter() - start)

        average = sum(timings) / len(timings)

        self.assertEqual(len(parsed_articles), 120)
        self.assertLess(
            average,
            threshold,
            msg=f"Average scrape time {average:.6f}s exceeded threshold {threshold:.6f}s",
        )


if __name__ == "__main__":
    unittest.main()
