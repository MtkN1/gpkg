import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen

from gpkg._package import Installer, Package


class Xh(Package):
    @property
    def owner(self) -> str:
        return "ducaale"

    @property
    def repo(self) -> str:
        return "xh"

    @property
    def command(self) -> str:
        return "xh"

    @property
    def machine_map(self) -> dict[str, str]:
        return {
            "x86_64": "x86_64",
        }

    def install(self, tag_name: str, *, prefix: Path) -> None:
        """e.g. curl -fsSL https://github.com/ducaale/xh/releases/download/v0.22.2/xh-v0.22.2-x86_64-unknown-linux-musl.tar.gz | tar -xz
        .
        └── xh-v0.22.2-x86_64-unknown-linux-musl
            ├── LICENSE
            ├── README.md
            ├── completions
            │   ├── _xh
            │   ├── _xh.ps1
            │   ├── xh.bash
            │   └── xh.fish
            ├── doc
            │   ├── CHANGELOG.md
            │   └── xh.1
            └── xh
        """

        owner = self.owner
        repo = self.repo
        command = self.command
        machine = self.machine
        libcname = "musl"  # NOTE: Is musl the only libc?
        url = f"https://github.com/{owner}/{repo}/releases/download/{tag_name}/{command}-{tag_name}-{machine}-unknown-linux-{libcname}.tar.gz"

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
            complete_path = Path(extracted_path, "completions", f"{command}.bash")
            man_path = Path(extracted_path, "doc", f"{command}.1")

            installer = Installer(prefix=prefix)
            installer.install_bin(bin_path)
            installer.install_completion(complete_path, command)
            installer.install_man(man_path)
