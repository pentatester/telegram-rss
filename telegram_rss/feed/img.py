import attr
from bs4 import Tag
from typing import Optional


@attr.dataclass
class Img:
    src: str
    alt: str = ""
    title: str = ""
    height: Optional[int] = None
    width: Optional[int] = None

    @classmethod
    def from_tag(cls, tag: Tag) -> "Img":
        return cls(
            alt=tag.attrs.get("alt"),
            src=tag.attrs.get("src"),
            title=tag.attrs.get("title"),
            height=tag.attrs.get("height"),
            width=tag.attrs.get("width"),
        )

    @property
    def a_hidden(self) -> str:
        return f'<a href="{self.src}">\u200c</a>'
