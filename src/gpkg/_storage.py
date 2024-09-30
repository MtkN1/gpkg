import json
from pathlib import Path
from typing import ClassVar, Self

from gpkg._models import PackageInfo, StorageType
from gpkg._utils import concat_owner_repo, separate_owner_repo


class Storage:
    file_path: ClassVar[Path] = Path("share", "gpkg", "storage.json")

    def __init__(self, *, prefix: Path) -> None:
        self._prefix = prefix

        self._data: StorageType = {}

    def get(self, package_info: PackageInfo) -> str:
        owner_repo = concat_owner_repo(package_info)
        return self._data.get(owner_repo, "")

    def list(self) -> list[PackageInfo]:
        return [separate_owner_repo(owner_repo) for owner_repo in self._data.keys()]

    def add(
        self, package_info: PackageInfo, tag_name: str, *, save: bool = True
    ) -> None:
        owner_repo = concat_owner_repo(package_info)
        self._data[owner_repo] = tag_name
        if save:
            self.save()

    @classmethod
    def load(cls, *, prefix: Path) -> Self:
        storage = cls(prefix=prefix)
        storage_path = prefix / cls.file_path
        if storage_path.exists():
            with storage_path.open("r", encoding="utf-8") as fp:
                data = json.load(fp)
            storage._data.update(data)

        return storage

    def save(self) -> None:
        storage_path = self._prefix / self.file_path
        storage_path.parent.mkdir(parents=True, exist_ok=True)
        with storage_path.open("w", encoding="utf-8") as fp:
            json.dump(self._data, fp)
