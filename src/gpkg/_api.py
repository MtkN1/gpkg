import json
from collections.abc import Callable
from pathlib import Path

from githubkit import GitHub, UnauthAuthStrategy

from gpkg._models import PackageInfo, Release, Status, Storage
from gpkg._registry import Registry


def show(package: PackageInfo, *, storage_factory: Callable[..., Storage]) -> Status:
    """Retrive local package status."""
    storage = storage_factory()
    owner_repo = f"{package.owner}/{package.repo}"
    version = storage.get(owner_repo, "")
    return Status(version=version, installed=bool(version))


def fetch(
    package: PackageInfo, *, release_factory: Callable[[str, str], Release]
) -> Release:
    """Fetch latest tag name from GitHub Releases."""
    return release_factory(package.owner, package.repo)


def install(*packages: PackageInfo, prefix: Path) -> None:
    """Install packages."""
    if not packages:
        packages = tuple(Registry.list())

    github = GitHub(auth=UnauthAuthStrategy())

    def get_latest_release(owner: str, repo: str) -> Release:
        nonlocal github
        return github.rest.repos.get_latest_release(owner, repo).parsed_data

    storage = load(prefix=prefix)

    for package_info in packages:
        if f"{package_info.owner}/{package_info.repo}" in storage:
            continue
        tag_name = fetch(package_info, release_factory=get_latest_release)
        package = Registry.get(package_info)()
        package.install(tag_name.tag_name, prefix=prefix)
        storage[f"{package_info.owner}/{package_info.repo}"] = tag_name.tag_name

    save(storage, prefix=prefix)


def upgrade(*, prefix: Path) -> None:
    """Upgrade installed packages."""
    github = GitHub(auth=UnauthAuthStrategy())

    def get_latest_release(owner: str, repo: str) -> Release:
        nonlocal github
        return github.rest.repos.get_latest_release(owner, repo).parsed_data

    storage = load(prefix=prefix)

    for owner_repo, tag_name in storage.items():
        owner, repo = owner_repo.split("/")
        package_info = PackageInfo(owner=owner, repo=repo)
        tag_name = fetch(package_info, release_factory=get_latest_release)
        if tag_name.tag_name == storage[owner_repo]:
            continue
        package = Registry.get(package_info)()
        package.install(tag_name.tag_name, prefix=prefix)
        storage[owner_repo] = tag_name.tag_name

    save(storage, prefix=prefix)


def load(*, prefix: Path) -> Storage:
    """Load storage."""
    storage_path = prefix / Path("share", "gpkg", "storage.json")

    if storage_path.exists():
        with storage_path.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    else:
        return {}


def save(storage: Storage, *, prefix: Path) -> None:
    """Save storage."""
    storage_path = prefix / Path("share", "gpkg", "storage.json")
    storage_path.parent.mkdir(parents=True, exist_ok=True)

    with storage_path.open("w", encoding="utf-8") as fp:
        json.dump(storage, fp)
