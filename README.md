# gpkg

** **In development** ** gpkg is a package installer tool that uses GitHub Releases as its source.

Currently, only Linux is supported.

## Concept

gpkg is a tool to install binaries from GitHub Releases. It downloads the binary of the target tool and places it in the appropriate location in the user's local environment. If there are bash completion files or man files, they are also installed.

The installation method varies depending on the software, so gpkg implements the installation method for each software. A list of supported software is in the `gpkg/_packages` directory.

## Installation

gpkg is a Python script, but it is not deployed to PyPI at the moment. It is only available from the GitHub repository.

## Usage

Install a package:
```bash
gpkg install sharkdp/bat
```

Install multiple packages:
```bash
gpkg install sharkdp/bat sharkdp/fd
```

Install all packages:
```bash
gpkg install
```

Upgrade all packages:
```bash
gpkg upgrade
```
