from feedparser import parse as parse_feed
from feedparser import FeedParserDict
from typing import List

from telegram_rss.config import Config, FeedConfig
from . import Entry, Channel


class FeedUpdater:
    def __init__(self, config: Config, feed_config: FeedConfig):
        self.config = config
        self.feed_config = feed_config

    def __call__(self) -> List[Channel]:
        return self.get_feeds()

    def get_new_feeds(self) -> List[Channel]:
        feeds: List[Channel] = list()
        return feeds

    def get_feeds(self):
        return parse_feed(self.feed_config.source)

    def get_local_feeds(self):
        pass

    @property
    def local_dir(self) -> str:
        pass
