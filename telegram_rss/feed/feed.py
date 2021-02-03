import attr
from collections import UserList
from feedparser import FeedParserDict
from typing import List, MutableSequence, Optional

from . import Entry, Channel


@attr.dataclass
class Feed(MutableSequence[Entry]):
    channel: Optional[Channel] = None
    items: List[Entry] = attr.ib(factory=list)

    def __attrs_post_init__(self) -> None:
        if isinstance(self.channel, dict):
            self.channel = Channel.from_dict(self.channel)
        elif isinstance(self.channel, Channel):
            pass
        else:
            self.channel = None

        items: List[Entry] = list()
        for item in self.items:
            if isinstance(item, dict):
                items.append(Entry.from_dict(item))
            elif isinstance(item, Entry):
                items.append(item)
            else:
                raise ValueError(
                    "item in items should be either dict or Entry instance"
                )
        self.items = items
        self.data = items

    @classmethod
    def from_feedparser(cls, feed: FeedParserDict) -> "Feed":
        return cls(channel=feed["channel"], items=feed["items"])

    def __bool__(self):
        return bool(self.data)

    def __contains__(self, item):
        return item in self.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self.data[i])
        else:
            return self.data[i]

    def __setitem__(self, i, item):
        self.data[i] = item

    def __delitem__(self, i):
        del self.data[i]

    def __add__(self, other):
        if isinstance(other, Feed):
            return self.__class__(self.data + other.data)
        elif isinstance(other, type(self.data)):
            return self.__class__(self.data + other)
        return self.__class__(self.data + list(other))

    def __copy__(self):
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)
        # Create a copy and avoid triggering descriptors
        inst.__dict__["data"] = self.__dict__["data"][:]
        return inst

    def append(self, item):
        self.data.append(item)

    def insert(self, i, item):
        self.data.insert(i, item)

    def pop(self, i=-1):
        return self.data.pop(i)

    def remove(self, item):
        self.data.remove(item)

    def clear(self):
        self.data.clear()

    def copy(self):
        return self.__class__(self)

    def count(self, item):
        return self.data.count(item)

    def index(self, item, *args):
        return self.data.index(item, *args)

    def reverse(self):
        self.data.reverse()

    def sort(self, *args, **kwds):
        self.data.sort(*args, **kwds)

    def extend(self, other):
        if isinstance(other, UserList):
            self.data.extend(other.data)
        else:
            self.data.extend(other)
