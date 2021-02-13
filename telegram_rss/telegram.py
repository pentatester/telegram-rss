import logging
from telegram import Bot, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from time import sleep
from typing import List

from telegram_rss.config import Config, FeedConfig
from telegram_rss.feed import Entry, FeedUpdater

logger = logging.getLogger(__name__)


def make_reply_markup(text: str, link: str):
    keyboard = [[InlineKeyboardButton(text=text, url=link)]]
    return InlineKeyboardMarkup(keyboard)


def send_message(
    bot: Bot,
    entry: Entry,
    chat_ids: List[int],
    updater: FeedUpdater,
    config: Config,
    feed_config: FeedConfig,
    message_delay: float,
):
    feed_chat_ids = feed_config.get_chat_ids()
    feed_chat_ids.extend(chat_ids)
    feed_chat_ids = list(set(feed_chat_ids))
    read_more = feed_config.read_more_button or config.read_more_button
    web_page_preview = feed_config.web_page_preview or config.web_page_preview

    message = config.template.render(
        entry=entry,
        channel=updater.channel,
        **config.template_data,
    )

    if read_more:
        reply_markup = make_reply_markup(read_more, entry.link)
    else:
        reply_markup = None

    notification = (
        config.notification
        if feed_config.notification is None
        else feed_config.notification
    )

    for chat_id in feed_chat_ids:
        bot.send_message(
            chat_id,
            text=message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=not web_page_preview,
            disable_notification=not notification,
        )
        sleep(message_delay)


def send_update(bot: Bot, config: Config):
    chat_ids = config.get_chat_ids()
    logger.debug(f"Sending update to {chat_ids}")
    for feed_config in config.feeds:
        if not feed_config.enable:
            logger.debug(f"{feed_config.name} feed disabled")
            continue
        message_delay = feed_config.message_delay or config.message_delay
        updater = FeedUpdater(feed_config)
        entries = updater.get_new_entries()
        if not entries:
            logger.debug(f"New feeds not found for {feed_config.name}")
            continue
        entries.reverse()
        logger.debug(f"Sending {len(entries)} feeds to {chat_ids}")

        for entry in entries:
            send_message(
                bot=bot,
                entry=entry,
                chat_ids=chat_ids,
                updater=updater,
                config=config,
                feed_config=feed_config,
                message_delay=message_delay,
            )
        sleep(message_delay)
