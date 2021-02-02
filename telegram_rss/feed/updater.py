import attr
import logging
import os

from feedparser import parse as parse_feed
from typing import List, Optional

from telegram_rss.config import FeedConfig
from telegram_rss.utils import save_as, get_default_directory, load_dict
from . import Entry, Channel, Feed


class FeedUpdater:
    def __init__(self, feed_config: FeedConfig, ext: str = ".json"):
        self.feed_config = feed_config
        self._feed: Optional[Feed] = None
        self._local_feed: Optional[Feed] = None
        self.local_file = os.path.join(
            get_default_directory(),
            "data",
            f"{self.feed_config.name}" + ext,
        )
        self.logger = logging.getLogger(feed_config.name)

    def __call__(self, save: bool = True) -> List[Entry]:
        return self.get_new_entries(save=save)

    def get_new_entries(self, save: bool = True) -> List[Entry]:
        entries: List[Entry] = list()
        if not self.feed or self.feed == self.local_feed:
            self.logger.info("No new feeds found")
            return entries
        for feed in self.feed:
            if feed not in self.local_feed:
                entries.append(feed)
        self.logger.info(f"Found new {len(entries)} feeds")
        if entries and save:
            self.save_feed(self.feed)
            self.logger.debug(f"Saved {len(entries)} as {self.local_file}")
        return entries

    @property
    def feed(self) -> Feed:
        if self._feed:
            return self._feed
        if self.feed_config.save_bandwith:
            raw_feed = parse_feed(
                self.feed_config.source,
                etag=self.feed_config.etag,
                modified=self.feed_config.modified,
            )
        else:
            raw_feed = parse_feed(self.feed_config.source)
        if raw_feed.status == 304:
            return Feed()
        self.feed_config.etag = raw_feed.etag
        self.feed_config.modified = raw_feed.modified
        self._feed = Feed.from_feedparser(raw_feed)
        return self._feed

    @property
    def local_feed(self) -> Feed:
        if self._local_feed:
            return self._local_feed
        if not os.path.isfile(self.local_file):
            return Feed()
        feed_data = load_dict(self.local_file)
        self._local_feed = Feed(**feed_data)
        return self._local_feed

    def save_feed(self, feed: Feed):
        feed_data = attr.asdict(feed, recurse=True)
        save_as(feed_data, self.local_file)

    @property
    def channel(self) -> Optional[Channel]:
        return self.feed.channel or self.local_feed.channel
