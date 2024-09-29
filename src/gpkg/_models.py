from typing import Protocol

from pydantic import BaseModel

type Storage = dict[str, str]


class Release(Protocol):
    tag_name: str


class PackageInfo(BaseModel, frozen=True):
    owner: str
    repo: str


class Status(BaseModel, frozen=True):
    version: str
    installed: bool
