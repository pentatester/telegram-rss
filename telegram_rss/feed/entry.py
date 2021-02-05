import attr
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser
from typing import List, Optional

from telegram_rss.utils import sanitize_text
from . import Img


@attr.dataclass
class Entry:
    title: str
    link: str
    description: str
    author: str
    published: Optional[str] = None

    def __attrs_post_init__(self) -> None:
        self._imgs: Optional[List[Img]] = None
        self._time: Optional[datetime] = None

    def __str__(self):
        return self.safe_title

    @property
    def time(self) -> Optional[datetime]:
        if self._time is not None:
            return self._time
        elif self.published is None:
            return None
        self._time = parser.parse(self.published) if self.published else None
        return self._time

    @property
    def imgs(self) -> List[Img]:
        if self._imgs is not None:
            return self._imgs
        self._imgs = list()
        soup = BeautifulSoup(self.description, "html.parser")
        for img in soup.find_all("img"):
            self._imgs.append(Img.from_tag(img))
        return self._imgs

    @property
    def safe_title(self) -> str:
        return sanitize_text(self.title)

    @property
    def safe_description(self) -> str:
        return sanitize_text(self.description)

    @property
    def clean_description(self) -> str:
        # Thanks https://stackoverflow.com/a/17610612
        return "\n".join(
            [ll.rstrip() for ll in self.safe_description.splitlines() if ll.strip()]
        )

    @classmethod
    def from_dict(cls, item: dict) -> "Entry":
        return cls(
            title=item["title"],
            link=item["link"],
            description=item["description"],
            author=item["author"],
            published=item.get("published"),
        )
