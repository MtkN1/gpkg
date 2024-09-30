import stat
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING
from urllib.request import urlopen

from gpkg._package import Installer, Package

if TYPE_CHECKING:
    from http.client import HTTPResponse


class Jq(Package):
    @property
    def owner(self) -> str:
        return "jqlang"

    @property
    def repo(self) -> str:
        return "jq"

    @property
    def command(self) -> str:
        return "jq"

    @property
    def machine_map(self) -> dict[str, str]:
        return {
            "x86_64": "amd64",
        }

    def install(self, tag_name: str, *, prefix: Path) -> None:
        """e.g. https://github.com/jqlang/jq/releases/download/jq-1.7.1/jq-linux-amd64"""

        owner = self.owner
        repo = self.repo
        command = self.command
        machine = self.machine
        url = f"https://github.com/{owner}/{repo}/releases/download/{tag_name}/{command}-linux-{machine}"

        response: HTTPResponse
        with (
            urlopen(url) as response,
            TemporaryDirectory() as tempdir,
        ):
            bin_path = Path(tempdir, command)

            with bin_path.open("wb") as executable:
                if chunk := response.read(1024):
                    executable.write(chunk)

            bin_path.chmod(bin_path.stat().st_mode | stat.S_IEXEC)

            installer = Installer(prefix=prefix)
            installer.install_bin(bin_path)
