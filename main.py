from scraper import Scraper

for article in Scraper().scrape():
    print(article.title)