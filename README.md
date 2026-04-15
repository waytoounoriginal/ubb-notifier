# UBB Notifier

Monitors <https://www.cs.ubbcluj.ro/> for new articles and sends push notifications via [ntfy.sh](https://ntfy.sh) when new content is found.

Seen article IDs are persisted in Upstash Redis, so the repository no longer needs to commit a state file after each run.

## Architecture

```
AWS Lambda
   │
   ▼
Python handler (main.py)
┌─────────────────────────────────────────────┐
│                                             │
│  Scraper ──► Repository ──► Notifier       │
│    │             │              │          │
│  Fetches     Tracks seen    Sends push     │
│  UBB CS      article IDs   notification    │
│  page       in Upstash      via ntfy.sh    │
└─────────────────────────────────────────────┘
```

1. **AWS Lambda** – Runs on a schedule and executes the Python handler directly.
2. **Scraper** (`scraper.py`) – Fetches the UBB CS homepage and parses article cards (`div[id^="post-"]`), extracting title, overview, and URL.
3. **Repository** (`repository.py`) – Uses a Redis set (`ubb_notifier:seen_article_ids`) to track already-seen article IDs and prevent duplicate notifications.
4. **Notifier** (`notifier.py`) – Sends a push notification for each new article using the [ntfy.sh](https://ntfy.sh) HTTP API. The topic name is supplied via the `NOTIFIER_TAG_NAME` secret.

## Scraper details

### What it extracts
- Containers: `div` elements with `id="post-<number>"`
- Title: `h2.title > a[title]` (link text)
- Overview: `div.entry` (inner text)
- URL: `href` attribute of the title link

### Entity
- `Article(title: str, overview: str, id_: str, url: str)` in `article.py`

## Deployment

Deploy as a Lambda function with the handler set to `main.lambda_handler`.

Required runtime dependencies:
- `requests`
- `beautifulsoup4`
- `redis`

## Secrets

Required environment variables:
- `NOTIFIER_TAG_NAME` – ntfy topic used for notifications.
- `REDIS_URL` – Upstash Redis connection URL, for example `rediss://default:<password>@<host>:<port>`.

Suggested Lambda configuration:
- Run on a schedule with Amazon EventBridge.
- Set a timeout long enough for the scrape + notification run.
- Keep the function in the same region as your Upstash endpoint if possible to reduce latency.

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
