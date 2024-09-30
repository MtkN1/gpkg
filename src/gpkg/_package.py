import shutil
from abc import ABC, abstractmethod
from pathlib import Path

from gpkg._platform import get_libcname, get_machine


class Package(ABC):
    @property
    @abstractmethod
    def owner(self) -> str: ...

    @property
    @abstractmethod
    def repo(self) -> str: ...

    @property
    def machine_map(self) -> dict[str, str]:
        return {}

    @property
    def machine(self) -> str:
        machine_map = self.machine_map

        machine = get_machine()
        if machine not in machine_map:
            raise ValueError(f"Unsupported machine: {machine}")
        return machine_map[machine]

    @property
    def libcname_map(self) -> dict[str, str]:
        return {}

    @property
    def libcname(self) -> str:
        libcname_map = self.libcname_map

        libcname = get_libcname()
        if libcname not in libcname_map:
            raise ValueError(f"Unsupported C library: {libcname}")
        return libcname_map[libcname]

    @abstractmethod
    def install(self, tag_name: str, *, prefix: Path) -> None: ...


class Installer:
    def __init__(self, prefix: Path):
        self._prefix = prefix

    def _install(self, src: Path, dst: Path) -> None:
        dst = self._prefix / dst
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    def install_bin(self, bin_path: Path) -> None:
        local_bin_path = Path("bin") / bin_path.name
        self._install(bin_path, local_bin_path)

    def install_completion(self, completion_path: Path, filename: str) -> None:
        local_completion_path = Path(
            "share", "bash-completion", "completions", filename
        )
        self._install(completion_path, local_completion_path)

    def install_man(self, man_path: Path) -> None:
        local_man_path = Path("share", "man", "man1") / man_path.name
        self._install(man_path, local_man_path)
