import attr
import os
import toml
from typing import List, Optional

from telegram_rss.utils import get_default_directory as _get_default_directory
from telegram_rss.utils import save_as


@attr.dataclass
class FeedConfig:
    name: str
    source: str
    cache: Optional[str] = None

    def __str__(self):
        return self.name


@attr.dataclass
class Config:
    bot_token: Optional[str] = None
    env_token: str = "TOKEN"
    config_dir: str = _get_default_directory()
    users: List[int] = attr.ib(factory=list)
    channels: List[int] = attr.ib(factory=list)
    feeds: List[FeedConfig] = attr.ib(factory=list)

    def __attr_post_init__(self) -> None:
        new_rss: List[FeedConfig] = list()
        for rss in self.feeds:
            if isinstance(rss, FeedConfig):
                new_rss.append(rss)
            elif isinstance(rss, dict):
                new_rss.append(FeedConfig(**rss))
        self.feeds = new_rss

    @property
    def token(self) -> str:
        if self.token:
            return self.token
        elif self.env_token:
            return os.environ.get(self.env_token, "")
        else:
            raise ValueError(
                f"either token or env_token must be filled in the config ({self.config_dir})"
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
