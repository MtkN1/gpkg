from typing import NamedTuple

type StorageType = dict[str, str]


class PackageInfo(NamedTuple):
    owner: str
    repo: str


class Status(NamedTuple):
    tag_name: str
