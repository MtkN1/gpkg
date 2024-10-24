from __future__ import annotations

import builtins
from collections.abc import Generator
from pathlib import Path
from typing import TYPE_CHECKING, Any

from gpkg._models import PackageInfo, Status
from gpkg._registry import Registry
from gpkg._storage import Storage

if TYPE_CHECKING:
    from githubkit import GitHub


def show(package_info: PackageInfo, *, storage: Storage) -> Status:
    """Retrive local package status."""

    tag_name = storage.get(package_info)
    return Status(tag_name=tag_name)


def list() -> builtins.list[PackageInfo]:
    """List all packages."""

    return Registry.list()


def fetch(package_info: PackageInfo, *, github: GitHub[Any]) -> str:
    """Fetch latest tag name from GitHub Releases."""

    response = github.rest.repos.get_latest_release(
        package_info.owner, package_info.repo
    )
    return response.parsed_data.tag_name


def install(*seq_package_info: PackageInfo, prefix: Path, github: GitHub[Any]) -> None:
    """Install packages."""

    if not seq_package_info:
        seq_package_info = tuple(Registry.list())

    storage = Storage.load(prefix=prefix)

    for package_info in seq_package_info:
        if storage.get(package_info):
            continue

        tag_name = fetch(package_info, github=github)

        package = Registry.get(package_info)()
        package.install(tag_name, prefix=prefix)

        storage.add(package_info, tag_name)


def upgrade(*, prefix: Path, github: GitHub[Any]) -> Generator[tuple[PackageInfo, str, str], None, None]:
    """Upgrade installed packages."""

    storage = Storage.load(prefix=prefix)

    for package_info in storage.list():
        current_tag_name = storage.get(package_info)
        latest_tag_name = fetch(package_info, github=github)
        if current_tag_name == latest_tag_name:
            continue

        package = Registry.get(package_info)()
        package.install(latest_tag_name, prefix=prefix)

        storage.add(package_info, latest_tag_name)

        yield package_info, current_tag_name, latest_tag_name

