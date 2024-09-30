import subprocess
import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen

from gpkg._package import Installer, Package


class Uv(Package):
    @property
    def owner(self) -> str:
        return "astral-sh"

    @property
    def repo(self) -> str:
        return "uv"

    @property
    def command(self) -> str:
        return "uv"

    @property
    def machine_map(self) -> dict[str, str]:
        return {
            "x86_64": "x86_64",
        }

    @property
    def libcname_map(self) -> dict[str, str]:
        return {
            "glibc": "gnu",
        }

    def install(self, tag_name: str, *, prefix: Path) -> None:
        """e.g. curl -fsSL https://github.com/astral-sh/uv/releases/download/0.4.17/uv-x86_64-unknown-linux-gnu.tar.gz | tar -xz
        .
        └── uv-x86_64-unknown-linux-gnu
            ├── uv
            └── uvx
        """

        owner = self.owner
        repo = self.repo
        command = self.command
        machine = self.machine
        libcname = self.libcname
        url = f"https://github.com/{owner}/{repo}/releases/download/{tag_name}/{command}-{machine}-unknown-linux-{libcname}.tar.gz"

        with (
            urlopen(url) as fileobj,
            tarfile.open(fileobj=fileobj, mode="r|gz") as tar,
            TemporaryDirectory() as tempdir,
        ):
            tar.extractall(tempdir, filter="data")

            extracted_path = Path(
                tempdir, f"{command}-{machine}-unknown-linux-{libcname}"
            )
            uv_bin_path = Path(extracted_path, command)
            uvx_bin_path = Path(extracted_path, f"{command}x")
            uv_complete_path = Path(extracted_path, f"{command}.bash")
            uvx_complete_path = Path(extracted_path, f"{command}x.bash")

            with uv_complete_path.open("w") as stdout:
                subprocess.run(
                    [uv_bin_path, "generate-shell-completion", "bash"],
                    stdout=stdout,
                    check=True,
                )
            with uvx_complete_path.open("w") as stdout:
                subprocess.run(
                    [uvx_bin_path, "--generate-shell-completion", "bash"],
                    stdout=stdout,
                    check=True,
                )

            installer = Installer(prefix=prefix)
            installer.install_bin(uv_bin_path)
            installer.install_bin(uvx_bin_path)
            installer.install_completion(uv_complete_path, command)
            installer.install_completion(uvx_complete_path, f"{command}x")
