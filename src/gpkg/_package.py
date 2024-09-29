import shutil
from pathlib import Path
from typing import Protocol


class Package(Protocol):
    def install(self, tag_name: str, *, prefix: Path) -> None: ...


class Installer:
    def __init__(self, prefix: Path):
        self._prefix = prefix

    def _install(self, src: Path, dst: Path) -> None:
        dst = self._prefix / dst
        dst.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    def install_bin(self, bin_path: Path) -> None:
        local_bin_path = Path("bin")
        self._install(bin_path, local_bin_path)

    def install_completion(self, completion_path: Path, filename: str) -> None:
        local_completion_path = Path(
            "share", "bash-completion", "completions", filename
        )
        self._install(completion_path, local_completion_path)

    def install_man(self, man_path: Path) -> None:
        local_man_path = Path("share", "man", "man1")
        self._install(man_path, local_man_path)
