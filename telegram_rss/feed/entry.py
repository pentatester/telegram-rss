import attr
from datetime import datetime
from telegram_rss.utils import sanitize_text


@attr.dataclass
class Entry:
    title: str
    link: str
    description: str
    author: str
    time: datetime

    def __str__(self):
        return self.t

    @property
    def safe_title(self) -> str:
        return sanitize_text(self.title)

    @property
    def safe_description(self) -> str:
        return sanitize_text(self.description)
