import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen

from gpkg._package import Installer, Package


class Ripgrep(Package):
    @property
    def owner(self) -> str:
        return "BurntSushi"

    @property
    def repo(self) -> str:
        return "ripgrep"

    @property
    def command(self) -> str:
        return "rg"

    @property
    def machine_map(self) -> dict[str, str]:
        return {
            "x86_64": "x86_64",
        }

    def install(self, tag_name: str, *, prefix: Path) -> None:
        # e.g. https://github.com/BurntSushi/ripgrep/releases/download/14.1.1/ripgrep-14.1.1-x86_64-unknown-linux-musl.tar.gz

        owner = self.owner
        repo = self.repo
        command = self.command
        machine = self.machine
        libcname = "musl"  # NOTE: Is musl the only libc?
        version = tag_name.removeprefix("v")
        url = f"https://github.com/{owner}/{repo}/releases/download/{tag_name}/{repo}-{version}-{machine}-unknown-linux-{libcname}.tar.gz"

        with (
            urlopen(url) as fileobj,
            tarfile.open(fileobj=fileobj, mode="r|gz") as tar,
            TemporaryDirectory() as tempdir,
        ):
            tar.extractall(tempdir, filter="data")

            extracted_path = Path(
                tempdir, f"{repo}-{version}-{machine}-unknown-linux-{libcname}"
            )
            bin_path = Path(extracted_path, command)
            complete_path = Path(extracted_path, "complete", f"{command}.bash")
            man_path = Path(extracted_path, "doc", f"{command}.1")

            installer = Installer(prefix=prefix)
            installer.install_bin(bin_path)
            installer.install_completion(complete_path, command)
            installer.install_man(man_path)
