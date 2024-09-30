from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

import gpkg

if TYPE_CHECKING:
    from githubkit import GitHub, UnauthAuthStrategy


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            gpkg.PackageInfo(owner="org", repo="not-installed-package"),
            gpkg.Status(tag_name=""),
        ),
        (
            gpkg.PackageInfo(owner="org", repo="installed-package"),
            gpkg.Status(tag_name="0.1.0"),
        ),
    ],
)
def test_show(
    tmp_path: Path, test_input: gpkg.PackageInfo, expected: gpkg.Status
) -> None:
    storage = gpkg.Storage(prefix=tmp_path)
    storage.add(gpkg.PackageInfo(owner="org", repo="installed-package"), "0.1.0")

    status = gpkg.show(test_input, storage=storage)

    assert status == expected


def test_fetch(github: GitHub[UnauthAuthStrategy]) -> None:
    # FIXME: It uses a real API and should be mocked
    tag_name = gpkg.fetch(gpkg.PackageInfo(owner="sharkdp", repo="bat"), github=github)

    assert tag_name == "v0.24.0" or tag_name >= "v0.24.0"


def test_install(tmp_path: Path, github: GitHub[UnauthAuthStrategy]) -> None:
    bat_pkg = gpkg.PackageInfo(owner="sharkdp", repo="bat")

    # FIXME: It uses a real API and should be mocked
    gpkg.install(bat_pkg, prefix=tmp_path, github=github)

    bin_path = tmp_path / "bin" / "bat"
    completion_path = tmp_path / "share" / "bash-completion" / "completions" / "bat"
    man_path = tmp_path / "share" / "man" / "man1" / "bat.1"
    assert (bin_path).exists()
    assert (completion_path).exists()
    assert (man_path).exists()


def test_upgrade(tmp_path: Path, github: GitHub[UnauthAuthStrategy]) -> None:
    # FIXME: It uses a real API and should be mocked
    gpkg.upgrade(prefix=tmp_path, github=github)
