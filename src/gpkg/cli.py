import builtins
from pathlib import Path
from typing import Annotated

import typer
from githubkit import GitHub, UnauthAuthStrategy
from rich.console import Console
from rich.table import Table

import gpkg

__all__ = ["app"]

app = typer.Typer()
console = Console()


@app.command()
def list() -> None:
    """List all packages in gpkg registry."""
    packages = gpkg.list()
    packages_json = [gpkg.concat_owner_repo(x) for x in packages]
    console.print_json(data=packages_json)


@app.command()
def install(
    packages: Annotated[builtins.list[str] | None, typer.Argument()] = None,
) -> None:
    """Install packages."""
    if packages is None:
        if typer.confirm("Do you want to install all packages?"):
            target_packages = gpkg.list()
        else:
            raise typer.Abort()
    else:
        target_packages = [gpkg.separate_owner_repo(x) for x in packages]

    prefix = Path.home() / ".local"
    with GitHub(UnauthAuthStrategy()) as github:
        for package_info in target_packages:
            # TODO: Show installation progress
            console.print(f"Installing {gpkg.concat_owner_repo(package_info)} ...")
            gpkg.install(package_info, prefix=prefix, github=github)


@app.command()
def upgrade() -> None:
    """Upgrade installed packages."""
    prefix = Path.home() / ".local"
    with GitHub(UnauthAuthStrategy()) as github:
        # TODO: Show upgrade progress
        console.print("Upgrading installed packages ...")
        gpkg.upgrade(prefix=prefix, github=github)


@app.command()
def show(
    package: Annotated[str | None, typer.Argument()] = None,
) -> None:
    """Show package status."""
    storage = gpkg.Storage(prefix=Path.home() / ".local")

    table = Table(title="Installed Packages")
    table.add_column("Package")
    table.add_column("Tag name")

    if package is not None:
        target_packages = [gpkg.separate_owner_repo(package)]
    else:
        target_packages = gpkg.list()

    for package_info in target_packages:
        status = gpkg.show(package_info, storage=storage)
        owner_repo = gpkg.concat_owner_repo(package_info)
        table.add_row(owner_repo, status.tag_name or "NOT INSTALLED")

    console.print(table)
