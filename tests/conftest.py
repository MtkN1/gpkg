from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from githubkit import GitHub, UnauthAuthStrategy

if TYPE_CHECKING:
    from collections.abc import Iterator


@pytest.fixture(scope="session")
def github() -> Iterator[GitHub[UnauthAuthStrategy]]:
    with GitHub(UnauthAuthStrategy()) as github:
        yield github
