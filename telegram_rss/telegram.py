import logging
from telegram import Bot, ParseMode
from time import sleep
from typing import List, Optional

from telegram_rss.config import Config
from telegram_rss.feed import Entry, Channel, FeedUpdater

logger = logging.getLogger(__name__)


def make_message(entry: Entry, channel: Optional[Channel] = None) -> str:
    if channel:
        return str(entry) + "\n" + f"<i>Channel</i>: {channel.title}"
    return str(entry)


def send_message(bot: Bot, text: str, chat_ids: List[int]):
    for chat_id in chat_ids:
        bot.send_message(chat_id, text, parse_mode=ParseMode.HTML)
        sleep(0.05)


def send_update(bot: Bot, config: Config):
    chat_ids = config.channels + config.users
    for feed_config in config.feeds:
        updater = FeedUpdater(feed_config)
        entries = updater.get_new_entries()
        entries.reverse()
        for entry in entries:
            message = make_message(entry, updater.channel)
            send_message(bot, message, chat_ids)
        sleep(3.0)
