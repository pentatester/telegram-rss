import attr
import logging
import os
import toml
from jinja2 import Template
from typing import List, Optional

from telegram_rss.template import TEMPLATE
from telegram_rss.utils import get_default_directory as _get_default_directory
from telegram_rss.utils import save_as

logger = logging.getLogger(__name__)

TEMPLATE_DATA = {
    "author": "Author",
    "source": "Source",
    "published": "Published",
}


@attr.dataclass
class FeedConfig:
    name: str
    source: str
    enable: bool = True
    save_bandwith: bool = True
    users: List[int] = attr.ib(factory=list)
    channels: List[int] = attr.ib(factory=list)
    groups: List[int] = attr.ib(factory=list)
    notification: Optional[bool] = None
    etag: Optional[str] = None
    modified: Optional[str] = None
    web_page_preview: Optional[bool] = None
    read_more_button: Optional[str] = None
    message_delay: Optional[float] = None
    cache: Optional[str] = None

    def __str__(self):
        return self.name

    def get_chat_ids(self) -> List[int]:
        return self.users + self.channels + self.groups


@attr.dataclass
class Config:
    bot_token: str = ""
    env_token: str = "TOKEN"
    notification: bool = True
    web_page_preview: bool = True
    message_delay: float = 0.05
    read_more_button: str = "Read more..."
    template_file: Optional[str] = None
    config_dir: str = _get_default_directory()
    data_dir: str = _get_default_directory("data")
    template_data: dict = attr.ib(default=TEMPLATE_DATA)
    users: List[int] = attr.ib(factory=list)
    channels: List[int] = attr.ib(factory=list)
    groups: List[int] = attr.ib(factory=list)
    feeds: List[FeedConfig] = attr.ib(factory=list)

    def __attrs_post_init__(self) -> None:
        new_rss: List[FeedConfig] = list()
        for rss in self.feeds:
            if isinstance(rss, FeedConfig):
                new_rss.append(rss)
            elif isinstance(rss, dict):
                new_rss.append(FeedConfig(**rss))
        self.feeds = new_rss
        if not self.template_file or not os.path.isfile(self.template_file):
            self.template_file = os.path.join(
                self.get_default_directory(), "template.html"
            )
            with open(self.template_file, "w") as f:
                f.write(TEMPLATE)
            self._template = Template(TEMPLATE)
        else:
            with open(self.template_file, "r") as f:
                self._template = Template(f.read())
        logger.debug(f"Loaded config {self}")

    def get_chat_ids(self) -> List[int]:
        return self.users + self.channels + self.groups

    @property
    def template(self) -> Template:
        return self._template

    @property
    def token(self) -> str:
        if self.bot_token:
            return self.bot_token
        elif self.env_token:
            return os.environ.get(self.env_token, "")
        else:
            raise ValueError(
                f"either bot_token or env_token must be filled in the config ({self.config_dir})"
            )

    get_default_directory = staticmethod(_get_default_directory)

    @classmethod
    def exist(cls, directory: Optional[str] = None) -> bool:
        filepath = cls._config_file(directory)
        return os.path.isfile(filepath)

    @classmethod
    def read(cls, directory: Optional[str] = None) -> "Config":
        config_file = cls._config_file(directory)
        if not os.path.isfile(config_file):
            cls._create(config_file)
            print(f"Please edit the configuration file at {config_file}")
            exit()
        configs = toml.load(config_file)
        configs["config_dir"] = config_file
        return cls(**configs)  # type: ignore

    @classmethod
    def _create(cls, directory: Optional[str] = None) -> "Config":
        config_file = cls._config_file(directory)
        config = Config(config_dir=config_file)
        configs = attr.asdict(config, recurse=True)
        save_as(configs, config_file)
        return config

    @classmethod
    def _config_file(cls, directory: Optional[str] = None, name="config.toml") -> str:
        if directory and not directory.endswith(".toml"):
            directory = os.path.join(directory, name)
        return directory or os.path.join(cls.get_default_directory(), name)

    def save(self, directory: Optional[str] = None):
        configs = attr.asdict(self, recurse=True)
        config_file = self._config_file(directory)
        save_as(configs, config_file)

    def __del__(self):
        return self.save(self.config_dir)
