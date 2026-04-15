from scraper import Scraper
from repository import Repository
from notifier import Notifier
from time import sleep


if __name__ == "__main__":
    repo: Repository = Repository()
    scraper: Scraper = Scraper()
    notifier: Notifier = Notifier()

    print("CURR TOPIC ID:", notifier._TOPIC)

    print("Scraping articles...")

    curr_articles = scraper.scrape()

    successful_adds = repo.add_all(curr_articles)

    print("Sending notifications...")

    for article in curr_articles:
        notifier.notify(article)

    print("Notifications sent")