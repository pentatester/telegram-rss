import os


def get_default_directory() -> str:
    ret = os.environ.get("TELEGRAM_RSS_HOME") or os.path.join(
        os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"),
        "telegram-rss",
    )
    return os.path.realpath(ret)
