import attr
import os
import toml

from feedparser import parse as parse_feed
from typing import List, Optional

from telegram_rss.config import Config, FeedConfig
from telegram_rss.utils import save_as
from . import Entry, Feed


class FeedUpdater:
    def __init__(self, config: Config, feed_config: FeedConfig):
        self.config = config
        self.feed_config = feed_config
        self._feed: Optional[Feed] = None
        self._local_feed: Optional[Feed] = None

    def __call__(self) -> List[Entry]:
        return self.get_new_entries()

    def get_new_entries(self) -> List[Entry]:
        entries: List[Entry] = list()
        if self.feed == self.local_feed:
            return entries
        for feed in self.feed:
            if feed not in self.local_feed:
                entries.append(feed)
        return entries

    @property
    def feed(self) -> Feed:
        if self._feed:
            return self._feed
        self._feed = Feed.from_feedparser(parse_feed(self.feed_config.source))
        return self._feed

    @property
    def local_feed(self) -> Feed:
        if self._local_feed:
            return self._local_feed
        feed_data = toml.load(self.local_file)
        self._local_feed = Feed(**feed_data)
        return self._local_feed

    def _save_feed(self, feed: Feed):
        feed_data = attr.asdict(feed, recurse=True)
        save_as(feed_data, self.local_file)

    @property
    def local_file(self) -> str:
        return os.path.join(self.config.config_dir, f"{self.feed_config.name}.toml")
