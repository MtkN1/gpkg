import argparse
from pathlib import Path

from githubkit import GitHub, UnauthAuthStrategy

from gpkg._api import install, upgrade
from gpkg._utils import separate_owner_repo


def cli() -> None:
    """Command-line interface.

    Examples:
    gpkg install sharkdp/bat
    gpkg install sharkdp/bat sharkdp/fd

    gpkg upgrade
    """
    parser = argparse.ArgumentParser(description="gpkg")
    parser.add_argument("--prefix", type=Path, default=Path.home() / ".local")
    subparsers = parser.add_subparsers(dest="command")

    install_parser = subparsers.add_parser("install")
    install_parser.add_argument("packages", nargs="*", type=separate_owner_repo)

    subparsers.add_parser("upgrade")

    args = parser.parse_args()

    with GitHub(UnauthAuthStrategy()) as github:
        if args.command == "install":
            if args.packages:
                install(*args.packages, prefix=args.prefix, github=github)
            else:
                install(prefix=args.prefix, github=github)

        elif args.command == "upgrade":
            upgrade(prefix=args.prefix, github=github)
