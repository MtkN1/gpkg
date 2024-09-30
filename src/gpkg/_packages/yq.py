import stat
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING
from urllib.request import urlopen

from gpkg._package import Installer, Package

if TYPE_CHECKING:
    from http.client import HTTPResponse


class Yq(Package):
    @property
    def owner(self) -> str:
        return "mikefarah"

    @property
    def repo(self) -> str:
        return "yq"

    @property
    def command(self) -> str:
        return "yq"

    @property
    def machine_map(self) -> dict[str, str]:
        return {
            "x86_64": "amd64",
        }

    def install(self, tag_name: str, *, prefix: Path) -> None:
        """e.g. https://github.com/mikefarah/yq/releases/download/v4.44.3/yq_linux_amd64"""

        owner = self.owner
        repo = self.repo
        command = self.command
        machine = self.machine
        url = f"https://github.com/{owner}/{repo}/releases/download/{tag_name}/{command}_linux_{machine}"

        response: HTTPResponse
        with (
            urlopen(url) as response,
            TemporaryDirectory() as tempdir,
        ):
            bin_path = Path(tempdir, command)

            with bin_path.open("wb") as executable:
                while chunk := response.read(1024):
                    executable.write(chunk)

            bin_path.chmod(
                bin_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
            )

            installer = Installer(prefix=prefix)
            installer.install_bin(bin_path)
