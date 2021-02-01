import attr
import os
from feedparser import parse as parse_feed
from typing import List

from telegram_rss.config import Config, FeedConfig
from telegram_rss.utils import sanitize_text, save_as


@attr.dataclass
class Feed:
    title: str
    link: str
    description: str

    def __attr_post_init__(self) -> None:
        self.title = sanitize_text(self.title)
        self.description = sanitize_text(self.description)

    def __str__(self):
        return self.title

    def save(self, directory: str):
        data = attr.asdict(self, recurse=True)
        filepath = os.path.join(directory, self.title, '.toml')
        save_as(data, filepath)


@attr.dataclass
class FeedUpdater:
    config: Config
    rss: FeedConfig

    def __call__(self):
        pass

    def get_new_feeds(self) -> List[Feed]:
        feeds: List[Feed] = list()
        return feeds

    def get_feeds(self):
        return parse_feed(self.rss.source)

    def get_local_feeds(self):
        pass

    @property
    def local_dir(self) -> str:
        pass
