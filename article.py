from dataclasses import dataclass

@dataclass(frozen=True)
class Article:
    id_: str
    url: str
    title: str
    overview: str
