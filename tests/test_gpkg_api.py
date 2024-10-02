from __future__ import annotations

import stat
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


def test_install_bat(tmp_path: Path, github: GitHub[UnauthAuthStrategy]) -> None:
    package_info = gpkg.PackageInfo(owner="sharkdp", repo="bat")

    # FIXME: It uses a real API and should be mocked
    gpkg.install(package_info, prefix=tmp_path, github=github)

    bin_path = tmp_path / "bin" / "bat"
    completion_path = tmp_path / "share" / "bash-completion" / "completions" / "bat"
    man_path = tmp_path / "share" / "man" / "man1" / "bat.1"
    assert bin_path.exists()
    assert completion_path.exists()
    assert man_path.exists()


def test_install_fd(tmp_path: Path, github: GitHub[UnauthAuthStrategy]) -> None:
    package_info = gpkg.PackageInfo(owner="sharkdp", repo="fd")

    # FIXME: It uses a real API and should be mocked
    gpkg.install(package_info, prefix=tmp_path, github=github)

    bin_path = tmp_path / "bin" / "fd"
    completion_path = tmp_path / "share" / "bash-completion" / "completions" / "fd"
    man_path = tmp_path / "share" / "man" / "man1" / "fd.1"
    assert bin_path.exists()
    assert completion_path.exists()
    assert man_path.exists()


def test_install_eza(tmp_path: Path, github: GitHub[UnauthAuthStrategy]) -> None:
    package_info = gpkg.PackageInfo(owner="eza-community", repo="eza")

    # FIXME: It uses a real API and should be mocked
    gpkg.install(package_info, prefix=tmp_path, github=github)

    bin_path = tmp_path / "bin" / "eza"
    completion_path = tmp_path / "share" / "bash-completion" / "completions" / "eza"
    man_path = tmp_path / "share" / "man" / "man1" / "eza.1"
    assert bin_path.exists()
    assert completion_path.exists()
    assert man_path.exists()


def test_install_ripgrep(tmp_path: Path, github: GitHub[UnauthAuthStrategy]) -> None:
    package_info = gpkg.PackageInfo(owner="BurntSushi", repo="ripgrep")

    # FIXME: It uses a real API and should be mocked
    gpkg.install(package_info, prefix=tmp_path, github=github)

    bin_path = tmp_path / "bin" / "rg"
    completion_path = tmp_path / "share" / "bash-completion" / "completions" / "rg"
    man_path = tmp_path / "share" / "man" / "man1" / "rg.1"
    assert bin_path.exists()
    assert completion_path.exists()
    assert man_path.exists()


def test_install_lsd(tmp_path: Path, github: GitHub[UnauthAuthStrategy]) -> None:
    package_info = gpkg.PackageInfo(owner="lsd-rs", repo="lsd")

    # FIXME: It uses a real API and should be mocked
    gpkg.install(package_info, prefix=tmp_path, github=github)

    bin_path = tmp_path / "bin" / "lsd"
    completion_path = tmp_path / "share" / "bash-completion" / "completions" / "lsd"
    man_path = tmp_path / "share" / "man" / "man1" / "lsd.1"
    assert bin_path.exists()
    assert completion_path.exists()
    assert man_path.exists()


def test_install_xh(tmp_path: Path, github: GitHub[UnauthAuthStrategy]) -> None:
    package_info = gpkg.PackageInfo(owner="ducaale", repo="xh")

    # FIXME: It uses a real API and should be mocked
    gpkg.install(package_info, prefix=tmp_path, github=github)

    bin_path = tmp_path / "bin" / "xh"
    completion_path = tmp_path / "share" / "bash-completion" / "completions" / "xh"
    man_path = tmp_path / "share" / "man" / "man1" / "xh.1"
    assert bin_path.exists()
    assert completion_path.exists()
    assert man_path.exists()


def test_install_starship(tmp_path: Path, github: GitHub[UnauthAuthStrategy]) -> None:
    package_info = gpkg.PackageInfo(owner="starship", repo="starship")

    # FIXME: It uses a real API and should be mocked
    gpkg.install(package_info, prefix=tmp_path, github=github)

    bin_path = tmp_path / "bin" / "starship"
    completion_path = (
        tmp_path / "share" / "bash-completion" / "completions" / "starship"
    )
    assert bin_path.exists()
    assert completion_path.exists()


def test_install_jq(tmp_path: Path, github: GitHub[UnauthAuthStrategy]) -> None:
    package_info = gpkg.PackageInfo(owner="jqlang", repo="jq")

    # FIXME: It uses a real API and should be mocked
    gpkg.install(package_info, prefix=tmp_path, github=github)

    bin_path = tmp_path / "bin" / "jq"
    assert bin_path.exists()
    assert stat.S_IMODE(bin_path.stat().st_mode) == 0o755


def test_install_yq(tmp_path: Path, github: GitHub[UnauthAuthStrategy]) -> None:
    package_info = gpkg.PackageInfo(owner="mikefarah", repo="yq")

    # FIXME: It uses a real API and should be mocked
    gpkg.install(package_info, prefix=tmp_path, github=github)

    bin_path = tmp_path / "bin" / "yq"
    assert bin_path.exists()
    assert stat.S_IMODE(bin_path.stat().st_mode) == 0o755


def test_upgrade(tmp_path: Path, github: GitHub[UnauthAuthStrategy]) -> None:
    # FIXME: It uses a real API and should be mocked
    gpkg.upgrade(prefix=tmp_path, github=github)
