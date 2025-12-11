# day 11

from functools import reduce
from pathlib import Path

from ..util import read_lines

script_dir = Path(__file__).resolve().parent


def parse(lines):
    return {words[0][:-1]: set(words[1:]) for words in (line.split() for line in lines)}


def count_paths(
    network: dict[str, set[str]], start: str, end: str, cache: dict = None
) -> list[tuple[str]]:
    if cache and start in cache:
        return cache[start]

    if start == end:
        return 1

    if start not in network:
        return 0

    if cache is None:
        cache = {}

    count = 0
    for neighbor in network[start]:
        res = count_paths(network, neighbor, end, cache=cache)
        cache[neighbor] = res
        count += res
    return count


def part1(fn: Path) -> None:
    lines = read_lines(fn)

    network = parse(lines)
    npaths = count_paths(network, 'you', 'out')
    print(npaths)


def part2(fn: Path) -> None:
    lines = read_lines(fn)

    network = parse(lines)
    npaths = (
        count_paths(network, 'svr', 'fft'),
        count_paths(network, 'fft', 'dac'),
        count_paths(network, 'dac', 'out'),
    )
    print(npaths)
    print(reduce(lambda a, b: a * b, npaths))


if __name__ == '__main__':
    part1(script_dir / 'test1.txt')
    part1(script_dir / 'input.txt')

    part2(script_dir / 'test2.txt')
    part2(script_dir / 'input.txt')
