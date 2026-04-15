import requests
import uuid
from article import Article


class Notifier:
    _TOPIC = "notificari-ubb"

    def notify(self, article: Article):
        Notifier._send_push_notification(article)
        

    @staticmethod
    def _send_push_notification(article: Article):
        headers = {
            "Title": article.title.encode('utf-8'),
            "Priority": "max",
            "Tags": "warning",
            "Click": article.url,
            "Actions": "view, Open AcademicInfo, https://academicinfo.ubbcluj.ro"
        }

        requests.post(f"https://ntfy.sh/{Notifier._TOPIC}", headers=headers, data=article.overview.encode('utf-8'))