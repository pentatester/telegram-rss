import os
from bleach import clean as clean_html

ALLOWED_TAGS = ["b", "i", "u", "s", "a", "code", "pre"]


def get_default_directory() -> str:
    ret = os.environ.get("TELEGRAM_RSS_HOME") or os.path.join(
        os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"),
        "telegram-rss",
    )
    return os.path.realpath(ret)


def sanitize_text(text: str) -> str:
    return clean_html(text, tags=ALLOWED_TAGS)
