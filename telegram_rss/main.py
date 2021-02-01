#!/usr/bin/env python
import click
import logging
import sys
from telegram import Bot
from telegram.ext import Updater

from telegram_rss.config import Config
from telegram_rss.commands import register_commands
from telegram_rss.telegram import send_update

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


class Context(click.Context):
    obj: Config


@click.group("telegram-rss")
@click.pass_context
def cli(ctx: Context):
    ctx.ensure_object(Config)


@cli.command("update")
@click.pass_context
def update(ctx: Context):
    bot = Bot(token=ctx.obj.token)
    send_update(bot=bot, config=ctx.obj)


@cli.command("polling")
@click.pass_context
def polling(ctx: Context):
    updater = Updater(token=ctx.obj.token)
    updater.dispatcher.bot_data["config"] = ctx.obj
    register_commands(updater.dispatcher)
    updater.start_polling()


def main():
    config = Config.read()
    sys.exit(cli(ctx=config))


if __name__ == "__main__":
    main()
