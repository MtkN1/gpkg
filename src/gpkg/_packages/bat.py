import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen

from gpkg._package import Installer, Package
from gpkg._platform import get_libcname, get_machine


class Bat(Package):
    @property
    def owner(self) -> str:
        return "sharkdp"

    @property
    def repo(self) -> str:
        return "bat"

    @property
    def machine(self) -> str:
        machine_map = {
            "x86_64": "x86_64",
        }

        machine = get_machine()
        if machine not in machine_map:
            raise ValueError(f"Unsupported machine: {machine}")
        return machine_map[machine]

    @property
    def libcname(self) -> str:
        libcname_map = {
            "glibc": "gnu",
        }

        libcname = get_libcname()
        if libcname not in libcname_map:
            raise ValueError(f"Unsupported C library: {libcname}")
        return libcname_map[libcname]

    def install(self, tag_name: str, *, prefix: Path) -> None:
        # e.g. https://github.com/sharkdp/bat/releases/download/v0.24.0/bat-v0.24.0-x86_64-unknown-linux-gnu.tar.gz

        owner = self.owner
        repo = self.repo
        machine = self.machine
        libcname = self.libcname
        url = f"https://github.com/{owner}/{repo}/releases/download/{tag_name}/bat-{tag_name}-{machine}-unknown-linux-{libcname}.tar.gz"

        with (
            urlopen(url) as fileobj,
            tarfile.open(fileobj=fileobj, mode="r|gz") as tar,
            TemporaryDirectory() as tempdir,
        ):
            tar.extractall(tempdir, filter="data")

            extracted_path = Path(
                tempdir, f"bat-{tag_name}-{machine}-unknown-linux-{libcname}"
            )
            bin_path = extracted_path / "bat"
            complete_path = extracted_path / "autocomplete" / "bat.bash"
            man_path = extracted_path / "bat.1"

            installer = Installer(prefix=prefix)
            installer.install_bin(bin_path)
            installer.install_completion(complete_path)
            installer.install_man(man_path)
