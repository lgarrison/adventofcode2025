from os import PathLike
from pathlib import Path


def read_lines(fn: str | PathLike[str]) -> list[str]:
    return Path(fn).read_text().splitlines()
