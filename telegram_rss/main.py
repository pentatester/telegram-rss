#!/usr/bin/env python
import click
import logging
import sys
from telegram import Bot
from telegram.ext import Updater
from typing import Optional

from telegram_rss.config import Config
from telegram_rss.commands import register_commands
from telegram_rss.telegram import send_update


def set_debug(debug: bool):
    log_format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        if debug
        else "%(name)s - %(message)s"
    )
    logging.basicConfig(
        format=log_format,
        level=logging.DEBUG if debug else logging.INFO,
    )


logger = logging.getLogger(__name__)


class Context(click.Context):
    obj: Config


@click.group("telegram-rss")
@click.pass_context
def cli(ctx: Context):
    ctx.ensure_object(Config)


@cli.command("update")
@click.option("--debug/--no-debug", default=False)
@click.option("--token", default=None, help="Telegram bot token")
@click.pass_context
def update(ctx: Context, debug: bool, token: Optional[str] = None):
    set_debug(debug)
    logger.debug("Starting bot")
    bot = Bot(token=token or ctx.obj.token)
    logger.debug("Sending update only")
    send_update(bot=bot, config=ctx.obj)


@cli.command("polling")
@click.option("--debug/--no-debug", default=False)
@click.option("--token", default=None, help="Telegram bot token")
@click.pass_context
def polling(ctx: Context, debug: bool, token: Optional[str] = None):
    set_debug(debug)
    logger.debug("Starting bot")
    updater = Updater(token=token or ctx.obj.token)
    updater.dispatcher.bot_data["config"] = ctx.obj
    logger.debug("Registering commands")
    register_commands(updater.dispatcher)
    updater.start_polling()


def main():
    config = Config.read()
    sys.exit(cli(obj=config))  # pylint: disable=E1123,E1120


if __name__ == "__main__":
    main()
