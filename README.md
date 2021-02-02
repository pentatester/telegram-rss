# Telegram RSS

[![PyPi Package Version](https://img.shields.io/pypi/v/telegram-rss)](https://pypi.org/project/telegram-rss/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/telegram-rss)](https://pypi.org/project/telegram-rss/)
[![LICENSE](https://img.shields.io/github/license/pentatester/telegram-rss)](https://github.com/pentatester/telegram-rss/blob/master/LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Mypy](https://img.shields.io/badge/Mypy-enabled-brightgreen)](https://github.com/python/mypy)

Fetch rss and send the latest update to telegram. **This project is still in active development**

## Usage

### Setup

- Make sure you have python installed.
- Open command line.
- Install `pip install --upgrade telegram-rss`
- Run `python -m telegram_rss`
- Add bot token, feeds, [user's id](#how-to-get-ids), and/or [channel's id](#how-to-get-ids) inside telegram-rss/config.toml
- Run `python -m telegram_rss update` to send initial update (*use personal id to send initial update*)

If your system support entry_points, you can execute `python -m telegram_rss` with `telegram-rss`.

## Checking update

Run `python -m telegram_rss update` to check and send the latest feeds

## Example config

```toml
bot_token = "987654321:ASDASDASD-1sda2eas3asd-91sdajh28j"
env_token = "TOKEN"
users = [ 123456789,]
channels = [ -123456789,]
[[feeds]]
name = "Feed example online"
source = "http://feedparser.org/docs/examples/atom10.xml"
[[feeds]]
name = "Feed example local"
source = "c:\\incoming\\atom10.xml"
```

## How to get token

Just create a new bot account using [@BotFather](https://t.me/BotFather). **Don't forget to add the bot as channel's admin**

## How to get ids

Send / forward a message (user or channel) to [@JsonDumpBot](https://t.me/JsonDumpBot)
