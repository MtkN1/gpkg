import subprocess
import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen

from gpkg._package import Installer, Package


class Starship(Package):
    @property
    def owner(self) -> str:
        return "starship"

    @property
    def repo(self) -> str:
        return "starship"

    @property
    def command(self) -> str:
        return "starship"

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
        """e.g. curl -fsSL https://github.com/starship/starship/releases/download/v1.20.1/starship-x86_64-unknown-linux-gnu.tar.gz | tar -xz
        .
        └── starship
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

            bin_path = Path(tempdir, command)
            complete_path = Path(tempdir, f"{command}.bash")

            with complete_path.open("w") as stdout:
                subprocess.run(
                    [bin_path, "completions", "bash"], stdout=stdout, check=True
                )

            installer = Installer(prefix=prefix)
            installer.install_bin(bin_path)
            installer.install_completion(complete_path, command)
