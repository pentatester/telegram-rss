import attr
import os
import toml

from feedparser import parse as parse_feed
from feedparser import FeedParserDict
from typing import List

from telegram_rss.config import Config, FeedConfig
from telegram_rss.utils import save_as
from . import Feed


class FeedUpdater:
    def __init__(self, config: Config, feed_config: FeedConfig):
        self.config = config
        self.feed_config = feed_config

    def __call__(self) -> List[Feed]:
        return self.get_feeds()

    def get_new_feeds(self) -> List[Feed]:
        feeds: List[Feed] = list()
        return feeds

    def get_feeds(self):
        return parse_feed(self.feed_config.source)

    def get_local_feed(self) -> Feed:
        feed_data = toml.load(self.local_file)
        return Feed(**feed_data)

    def _save_feed(self, feed: Feed):
        feed_data = attr.asdict(feed, recurse=True)
        save_as(feed_data, self.local_file)

    @property
    def local_file(self) -> str:
        return os.path.join(self.config.config_dir, f"{self.feed_config.name}.toml")
