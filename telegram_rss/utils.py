import codecs
import os
import json
import toml
from bleach import clean as clean_html
from datetime import datetime
from pathlib import Path
from time import mktime, struct_time

ALLOWED_TAGS = ["b", "i", "u", "s", "a", "code", "pre"]


def get_default_directory(*args: str) -> str:
    ret = os.environ.get("TELEGRAM_RSS_HOME") or os.path.join(
        os.environ.get("XDG_CACHE_HOME") or os.getcwd(),
        "telegram-rss",
    )
    # os.path.expanduser("~/.cache")
    folders = os.path.join(os.path.realpath(ret), *args)
    Path(folders).mkdir(parents=True, exist_ok=True)
    return folders


def sanitize_text(text: str) -> str:
    return clean_html(text, tags=ALLOWED_TAGS, strip=True)


def save_as(data: dict, filepath: str):
    if filepath.endswith(".json"):
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
    elif filepath.endswith(".toml"):
        with open(filepath, "w") as f:
            toml.dump(data, f)
    else:
        raise ValueError(f"{filepath} should be *.json or *.toml")


def load_dict(filepath: str):
    data = None
    if filepath.endswith(".json"):
        with codecs.open(filepath) as f:
            data = json.load(f)
    elif filepath.endswith(".toml"):
        with codecs.open(filepath) as f:
            data = toml.load(f)
    else:
        raise ValueError(f"{filepath} should be *.json or *.toml")
    return data


def struct_time_to_datetime(struct: struct_time) -> datetime:
    # Thank you! https://stackoverflow.com/a/1697907
    return datetime.fromtimestamp(mktime(struct))
