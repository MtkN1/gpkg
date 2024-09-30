import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen

from gpkg._package import Installer, Package


class Bat(Package):
    @property
    def owner(self) -> str:
        return "sharkdp"

    @property
    def repo(self) -> str:
        return "bat"

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
            installer.install_completion(complete_path, "bat")
            installer.install_man(man_path)
