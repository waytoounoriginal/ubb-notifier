from article import Article
import redis
import os


class Repository:
    _SEEN_IDS_KEY = "ubb_notifier:seen_article_ids"
    _ARTICLE_LIMIT = 10 # to keep under upstash threshold


    def __init__(self):
        redis_url = os.environ.get("REDIS_URL")
        if not redis_url:
            raise RuntimeError("REDIS_URL environment variable is required")

        self._redis = redis.Redis.from_url(redis_url, decode_responses=True)


    def add_all(self, articles: list[Article]) -> list[Article]:
        successful_adds = []

        seen_articles_ids = self._redis.smembers(self._SEEN_IDS_KEY)

        for article in articles[:Repository._ARTICLE_LIMIT]:
            if article.id_ in seen_articles_ids:
                continue

            successful_adds.append(article)

            self._redis.sadd(self._SEEN_IDS_KEY, article.id_)

        return successful_adds
    

    def in_(self, id_: str):
        return self._redis.sismember(self._SEEN_IDS_KEY, id_)
    