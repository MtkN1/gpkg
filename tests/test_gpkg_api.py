from dataclasses import dataclass
from pathlib import Path

import pytest

import gpkg


@pytest.fixture
def not_installed_package() -> str:
    return "foo"


@pytest.fixture
def installed_package() -> str:
    return "bar"


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            gpkg.PackageInfo(owner="org", repo="not-installed-package"),
            gpkg.Status(version="", installed=False),
        ),
        (
            gpkg.PackageInfo(owner="org", repo="installed-package"),
            gpkg.Status(version="0.1.0", installed=True),
        ),
    ],
)
def test_show(test_input: gpkg.PackageInfo, expected: gpkg.Status) -> None:
    storage: gpkg.Storage = {"org/installed-package": "0.1.0"}

    status = gpkg.show(test_input, storage_factory=lambda: storage)

    assert status == expected


def test_fetch() -> None:
    @dataclass
    class Release:
        tag_name: str

    def fetch_release(owner: str, repo: str) -> gpkg.Release:
        test_input: dict[str, str] = {
            "owner/foo": "v0.1.0",
            "owner/bar": "v0.2.0",
        }
        return Release(tag_name=test_input[f"{owner}/{repo}"])

    release = gpkg.fetch(
        gpkg.PackageInfo(owner="owner", repo="foo"),
        release_factory=fetch_release,
    )

    assert release.tag_name == "v0.1.0"


def test_install(tmp_path: Path) -> None:
    gpkg.install(prefix=tmp_path)


def test_upgrade(tmp_path: Path) -> None:
    gpkg.upgrade(prefix=tmp_path)


def test_bat(tmp_path: Path) -> None:
    bat = gpkg.Bat()
    bat.install("v0.24.0", prefix=tmp_path)

    assert (tmp_path / "bin" / "bat").exists()
    assert (tmp_path / "share" / "bash-completion" / "completions" / "bat").exists()
    assert (tmp_path / "share" / "man" / "man1" / "bat.1").exists()
