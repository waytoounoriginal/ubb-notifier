from article import Article
import os


class Repository:
    _DATABASE_PATH = "./id_db.db"
    _DELIM = ';'


    def __init__(self):
        self._db_file_init()
        self._db_load()

        self._article_list = []


    def _db_file_init(self):
        if os.path.exists(self._DATABASE_PATH):
            return
        
        open(self._DATABASE_PATH, "w").close()
        

    def _db_load(self):
        self._id_set = set()

        with open(self._DATABASE_PATH, "r") as file:
            line = file.readline().strip()

        for id_ in line.split(sep=self._DELIM):
            self._id_set.add(id_)


    def add_all(self, articles: list[Article]) -> list[Article]:
        successful_adds = []

        for article in articles:
            if article.id_ in self._id_set:
                continue

            self._article_list.append(article)
            self._id_set.add(article.id_)
            successful_adds.append(article)

        with open(self._DATABASE_PATH, "w") as f:
            f.write(self._DELIM.join(id_ for id_ in self._id_set))

        return successful_adds
    

    def in_(self, id_: str):
        return id_ in self._id_set
    