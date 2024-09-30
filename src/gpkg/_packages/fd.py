import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen

from gpkg._package import Installer, Package
from gpkg._platform import get_libcname, get_machine


class Fd(Package):
    @property
    def owner(self) -> str:
        return "sharkdp"

    @property
    def repo(self) -> str:
        return "fd"

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
        # e.g. https://github.com/sharkdp/fd/releases/download/v10.2.0/fd-v10.2.0-x86_64-unknown-linux-gnu.tar.gz

        owner = self.owner
        repo = self.repo
        machine = self.machine
        libcname = self.libcname
        url = f"https://github.com/{owner}/{repo}/releases/download/{tag_name}/fd-{tag_name}-{machine}-unknown-linux-{libcname}.tar.gz"

        with (
            urlopen(url) as fileobj,
            tarfile.open(fileobj=fileobj, mode="r|gz") as tar,
            TemporaryDirectory() as tempdir,
        ):
            tar.extractall(tempdir, filter="data")

            extracted_path = Path(
                tempdir, f"fd-{tag_name}-{machine}-unknown-linux-{libcname}"
            )
            bin_path = extracted_path / "fd"
            complete_path = extracted_path / "autocomplete" / "fd.bash"
            man_path = extracted_path / "fd.1"

            installer = Installer(prefix=prefix)
            installer.install_bin(bin_path)
            installer.install_completion(complete_path, "fd")
            installer.install_man(man_path)
