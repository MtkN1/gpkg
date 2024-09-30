import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen

from gpkg._package import Installer, Package


class Eza(Package):
    @property
    def owner(self) -> str:
        return "eza-community"

    @property
    def repo(self) -> str:
        return "eza"

    @property
    def command(self) -> str:
        return "eza"

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
        # e.g. https://github.com/eza-community/eza/releases/download/v0.20.0/eza_x86_64-unknown-linux-gnu.tar.gz

        owner = self.owner
        repo = self.repo
        command = self.command
        machine = self.machine
        libcname = self.libcname
        version = tag_name.removeprefix("v")
        base_url = f"https://github.com/{owner}/{repo}/releases/download/{tag_name}"
        bin_url = base_url + f"/{command}_{machine}-unknown-linux-{libcname}.tar.gz"
        completion_url = base_url + f"/completions-{version}.tar.gz"
        man_url = base_url + f"/man-{version}.tar.gz"

        with (
            urlopen(bin_url) as bin_fileobj,
            tarfile.open(fileobj=bin_fileobj, mode="r|gz") as bin_tar,
            urlopen(completion_url) as completion_fileobj,
            tarfile.open(fileobj=completion_fileobj, mode="r|gz") as completion_tar,
            urlopen(man_url) as man_fileobj,
            tarfile.open(fileobj=man_fileobj, mode="r|gz") as man_tar,
            TemporaryDirectory() as tempdir,
        ):
            bin_tar.extractall(tempdir, filter="data")
            completion_tar.extractall(tempdir, filter="data")
            man_tar.extractall(tempdir, filter="data")

            bin_path = Path(tempdir, command)
            complete_path = Path(tempdir, "target", f"completions-{version}", command)
            man_path = Path(tempdir, "target", f"man-{version}", f"{command}.1")

            installer = Installer(prefix=prefix)
            installer.install_bin(bin_path)
            installer.install_completion(complete_path, command)
            installer.install_man(man_path)
