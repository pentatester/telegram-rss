import attr
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List

from telegram_rss.utils import sanitize_text
from . import Img


@attr.dataclass
class Entry:
    title: str
    link: str
    description: str
    author: str
    time: datetime
    imgs: List[Img] = attr.ib(factory=list)

    def __attrs_post_init__(self) -> None:
        soup = BeautifulSoup(self.description, "html.parser")
        for img in soup.find_all("img"):
            self.imgs.append(Img.from_tag(img))

    def __str__(self):
        return self.t

    @property
    def safe_title(self) -> str:
        return sanitize_text(self.title)

    @property
    def safe_description(self) -> str:
        return sanitize_text(self.description)
