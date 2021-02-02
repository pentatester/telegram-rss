import logging
from telegram import Bot, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from time import sleep
from typing import List, Optional

from telegram_rss.config import Config, FeedConfig
from telegram_rss.feed import Entry, Channel, FeedUpdater

logger = logging.getLogger(__name__)


def make_message(entry: Entry, channel: Optional[Channel] = None) -> str:
    if channel:
        return str(entry) + "\n" + f"<i>Channel</i>: {channel.title}"
    return str(entry)


def make_reply_markup(text: str, link: str):
    keyboard = [[InlineKeyboardButton(text=text, url=link)]]
    return InlineKeyboardMarkup(keyboard)


def send_message(
    bot: Bot,
    entry: Entry,
    chat_ids: List[int],
    config: FeedConfig,
    channel: Optional[Channel] = None,
    delay: float = 0.05,
    web_page_preview: bool = True,
    read_more: Optional[str] = None,
):
    message = make_message(entry, channel)
    if read_more:
        reply_markup = make_reply_markup(read_more, entry.link)
    else:
        reply_markup = None
    for chat_id in chat_ids:
        bot.send_message(
            chat_id,
            text=message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=not web_page_preview,
        )
        sleep(delay)


def send_update(bot: Bot, config: Config):
    chat_ids = config.channels + config.users
    for feed_config in config.feeds:
        updater = FeedUpdater(feed_config)
        entries = updater.get_new_entries()
        if not entries:
            continue
        entries.reverse()

        message_delay = feed_config.message_delay or config.message_delay
        read_more_button = feed_config.read_more_button or config.read_more_button

        for entry in entries:
            send_message(
                bot=bot,
                entry=entry,
                chat_ids=chat_ids,
                channel=updater.channel,
                config=feed_config,
                delay=message_delay,
                read_more=read_more_button,
            )
        sleep(message_delay)
