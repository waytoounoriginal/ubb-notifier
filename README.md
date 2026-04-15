# UBB Notifier

Monitors <https://www.cs.ubbcluj.ro/> for new articles and sends push notifications via [ntfy.sh](https://ntfy.sh) when new content is found.

Seen article IDs are persisted in Redis, so the repository no longer needs to commit a state file after each run.

## Architecture

```
AWS Lambda (scheduler)
        │
        │  POST /repos/.../actions/workflows/main.yml/dispatches
        ▼
GitHub Actions (workflow_dispatch)
        │
        ▼
   Python Script (main.py)
   ┌────────────────────────────────────────┐
   │                                        │
   │  Scraper ──► Repository ──► Notifier   │
   │    │             │              │      │
   │  Fetches     Tracks seen    Sends push │
   │  UBB CS      article IDs   notification│
   │  page        in Redis      via ntfy.sh │
   └────────────────────────────────────────┘
```

1. **AWS Lambda** – Runs on a schedule and triggers the GitHub Actions workflow via a POST request to the GitHub API (`workflow_dispatch` event).
2. **GitHub Actions** (`main.yml`) – Checks out the repo, installs dependencies, and runs `main.py` with `NOTIFIER_TAG_NAME` and `REDIS_URL` secrets.
3. **Scraper** (`scraper.py`) – Fetches the UBB CS homepage and parses article cards (`div[id^="post-"]`), extracting title, overview, and URL.
4. **Repository** (`repository.py`) – Uses a Redis set (`ubb_notifier:seen_article_ids`) to track already-seen article IDs and prevent duplicate notifications.
5. **Notifier** (`notifier.py`) – Sends a push notification for each new article using the [ntfy.sh](https://ntfy.sh) HTTP API. The topic name is supplied via the `NOTIFIER_TAG_NAME` secret.

## Scraper details

### What it extracts
- Containers: `div` elements with `id="post-<number>"`
- Title: `h2.title > a[title]` (link text)
- Overview: `div.entry` (inner text)
- URL: `href` attribute of the title link

### Entity
- `Article(title: str, overview: str, id_: str, url: str)` in `article.py`

## Workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| `main.yml` | `workflow_dispatch` (invoked by AWS Lambda) | Scrape, notify, and update seen IDs in Redis |
| `cleanup-db.yml` | `workflow_dispatch` (manual) | Clear Redis seen-article IDs key |

## Secrets

Required GitHub Actions secrets:
- `NOTIFIER_TAG_NAME` – ntfy topic used for notifications.
- `REDIS_URL` – Redis connection URL, for example `redis://:<password>@<host>:6379/0`.

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
