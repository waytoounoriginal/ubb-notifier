from scraper import Scraper
from repository import Repository
from notifier import Notifier
from time import sleep

# Globals so that they can be reused by lambdas
repo: Repository = Repository()
scraper: Scraper = Scraper()
notifier: Notifier = Notifier()

def lambda_handler(event, context):
    global repo, scraper, notifier

    print("CURR TOPIC ID:", notifier._TOPIC)

    print("Scraping articles...")

    curr_articles = scraper.scrape()

    new_articles = repo.add_all(curr_articles)

    print("Sending notifications...")

    for article in new_articles:
        notifier.notify(article)

    print("Notifications sent")

    return {
        'statusCode': 200,
        'body': f'UBB has been scrapped!'
    }