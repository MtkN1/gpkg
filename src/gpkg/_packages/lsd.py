import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen

from gpkg._package import Installer, Package


class Lsd(Package):
    @property
    def owner(self) -> str:
        return "lsd-rs"

    @property
    def repo(self) -> str:
        return "lsd"

    @property
    def command(self) -> str:
        return "lsd"

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
        """e.g. https://github.com/lsd-rs/lsd/releases/download/v1.1.5/lsd-v1.1.5-x86_64-unknown-linux-gnu.tar.gz
        .
        └── lsd-v1.1.5-x86_64-unknown-linux-gnu
            ├── LICENSE
            ├── README.md
            ├── autocomplete
            │   ├── _lsd
            │   ├── _lsd.ps1
            │   ├── lsd.bash-completion
            │   └── lsd.fish
            ├── lsd
            └── lsd.1
        """

        owner = self.owner
        repo = self.repo
        command = self.command
        machine = self.machine
        libcname = self.libcname
        url = f"https://github.com/{owner}/{repo}/releases/download/{tag_name}/{repo}-{tag_name}-{machine}-unknown-linux-{libcname}.tar.gz"

        with (
            urlopen(url) as fileobj,
            tarfile.open(fileobj=fileobj, mode="r|gz") as tar,
            TemporaryDirectory() as tempdir,
        ):
            tar.extractall(tempdir, filter="data")

            extracted_path = Path(
                tempdir, f"{command}-{tag_name}-x86_64-unknown-linux-{libcname}"
            )
            bin_path = Path(extracted_path, command)
            complete_path = Path(
                extracted_path, "autocomplete", f"{command}.bash-completion"
            )
            man_path = Path(extracted_path, f"{command}.1")

            installer = Installer(prefix=prefix)
            installer.install_bin(bin_path)
            installer.install_completion(complete_path, command)
            installer.install_man(man_path)
