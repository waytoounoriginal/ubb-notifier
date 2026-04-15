# UBB Notifier Scraper

Scrapes article cards from <https://www.cs.ubbcluj.ro/>.

## What it extracts
- Containers: `div` elements with `id="post-<number>"`
- Title: `h2.title > a[title]` (`title` attribute)
- Overview: `div.entry` (inner text)

## Entity
- `Article(title: str, overview: str)` in `article.py`

## Usage
```python
from scraper import Scraper

scraper = Scraper()
articles = scraper.scrape()

for article in articles:
    print(article.title)
    print(article.overview)
    print("-" * 40)
```

## Benchmark Tests
Run the benchmark-focused tests with:

```powershell
python -m unittest tests.test_benchmark -v
```

Optional environment variables:
- `BENCHMARK_PARSE_RUNS` (default: `40`)
- `BENCHMARK_PARSE_AVG_THRESHOLD_SEC` (default: `0.035`)
- `BENCHMARK_SCRAPE_RUNS` (default: `30`)
- `BENCHMARK_SCRAPE_AVG_THRESHOLD_SEC` (default: `0.045`)
