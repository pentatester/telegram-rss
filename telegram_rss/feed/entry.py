import attr
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Optional

from telegram_rss.utils import sanitize_text, struct_time_to_datetime
from . import Img


@attr.dataclass
class Entry:
    title: str
    link: str
    description: str
    author: str
    time: Optional[datetime] = None
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

    @classmethod
    def from_dict(cls, item: dict) -> "Entry":
        time = item.get('published_parsed')
        return cls(
            title=item["title"],
            link=item["link"],
            description=item["description"],
            author=item["author"],
            time=struct_time_to_datetime(time) if time else None,
        )
