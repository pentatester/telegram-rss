import attr
from telegram_rss.utils import sanitize_text


@attr.dataclass
class Channel:
    title: str
    link: str
    description: str

    def __str__(self):
        return self.title

    @property
    def safe_title(self) -> str:
        return sanitize_text(self.title)

    @property
    def safe_description(self) -> str:
        return sanitize_text(self.description)
