# UBB Notifier

Monitors <https://www.cs.ubbcluj.ro/> for new articles and sends push notifications via [ntfy.sh](https://ntfy.sh) when new content is found.

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
   │  page        in id_db.db   via ntfy.sh │
   └────────────────────────────────────────┘
        │
        ▼
   Persist id_db.db back to repo (git commit)
```

1. **AWS Lambda** – Runs on a schedule and triggers the GitHub Actions workflow via a POST request to the GitHub API (`workflow_dispatch` event).
2. **GitHub Actions** (`main.yml`) – Checks out the repo, installs dependencies, and runs `main.py`. After the script finishes, it commits any changes to `id_db.db` back to the repository.
3. **Scraper** (`scraper.py`) – Fetches the UBB CS homepage and parses article cards (`div[id^="post-"]`), extracting title, overview, and URL.
4. **Repository** (`repository.py`) – Reads and writes `id_db.db`, a flat file that tracks already-seen article IDs to prevent duplicate notifications.
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
| `main.yml` | `workflow_dispatch` (invoked by AWS Lambda) | Scrape, notify, persist seen IDs |
| `cleanup-db.yml` | `workflow_dispatch` (manual) | Delete `id_db.db` to reset seen-article history |

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
