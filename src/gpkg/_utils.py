from gpkg._models import PackageInfo


def concat_owner_repo(package_info: PackageInfo) -> str:
    return f"{package_info.owner}/{package_info.repo}"


def separate_owner_repo(owner_repo: str) -> PackageInfo:
    return PackageInfo(*owner_repo.split("/"))
