#!/bin/bash

set -eu

tempdir=$(mktemp -d)
cd "${tempdir}"

echo Downloading temporary uv binary ...
curl -fsSL https://github.com/astral-sh/uv/releases/download/0.4.17/uv-x86_64-unknown-linux-gnu.tar.gz | tar -xz --strip-components=1

echo Installing gpkg by temporary uv ...
./uv tool install 'git+https://github.com/MtkN1/gpkg'

echo Installing uv by gpkg ...
./uv tool run gpkg install astral-sh/uv

rm -rf "${tempdir}"
