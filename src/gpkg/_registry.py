from typing import ClassVar

from gpkg._models import PackageInfo
from gpkg._package import Package
from gpkg._packages.bat import Bat
from gpkg._packages.fd import Fd


class Registry:
    data: ClassVar[dict[PackageInfo, type[Package]]] = {
        PackageInfo(owner="sharkdp", repo="bat"): Bat,
        PackageInfo(owner="sharkdp", repo="fd"): Fd,
    }

    @classmethod
    def get(cls, package: PackageInfo) -> type[Package]:
        return cls.data[package]

    @classmethod
    def list(cls) -> list[PackageInfo]:
        return list(cls.data.keys())
