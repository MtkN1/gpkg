from typing import ClassVar

from gpkg._models import PackageInfo
from gpkg._package import Package
from gpkg._packages.bat import Bat
from gpkg._packages.eza import Eza
from gpkg._packages.fd import Fd
from gpkg._packages.jq import Jq
from gpkg._packages.lsd import Lsd
from gpkg._packages.ripgrep import Ripgrep
from gpkg._packages.starship import Starship
from gpkg._packages.xh import Xh
from gpkg._packages.yq import Yq


class Registry:
    data: ClassVar[dict[PackageInfo, type[Package]]] = {
        PackageInfo(owner="sharkdp", repo="bat"): Bat,
        PackageInfo(owner="sharkdp", repo="fd"): Fd,
        PackageInfo(owner="eza-community", repo="eza"): Eza,
        PackageInfo(owner="BurntSushi", repo="ripgrep"): Ripgrep,
        PackageInfo(owner="lsd-rs", repo="lsd"): Lsd,
        PackageInfo(owner="ducaale", repo="xh"): Xh,
        PackageInfo(owner="starship", repo="starship"): Starship,
        PackageInfo(owner="jqlang", repo="jq"): Jq,
        PackageInfo(owner="mikefarah", repo="yq"): Yq,
    }

    @classmethod
    def get(cls, package: PackageInfo) -> type[Package]:
        return cls.data[package]

    @classmethod
    def list(cls) -> list[PackageInfo]:
        return list(cls.data.keys())
