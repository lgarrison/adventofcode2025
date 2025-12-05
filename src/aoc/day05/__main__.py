# day 05

from pathlib import Path

from ..util import read_lines

script_dir = Path(__file__).resolve().parent


def overlap(r1: range, r2: range) -> bool:
    return r1.start < r2.stop and r2.start < r1.stop


def union(r1: range, r2: range) -> range:
    return range(min(r1.start, r2.start), max(r1.stop, r2.stop))


def part1(fn: Path) -> None:
    lines = read_lines(fn)
    s = lines.index('')
    ranges, ingredients = lines[:s], lines[s + 1 :]

    ranges = [
        range(start, end + 1) for start, end in (map(int, r.split('-')) for r in ranges)
    ]
    ingredients = [int(i) for i in ingredients]

    print(sum(1 for ingredient in ingredients if any(ingredient in r for r in ranges)))


def part2(fn: Path) -> None:
    lines = read_lines(fn)

    lines = read_lines(fn)
    s = lines.index('')
    ranges, ingredients = lines[:s], lines[s + 1 :]

    ranges = [
        range(start, end + 1) for start, end in (map(int, r.split('-')) for r in ranges)
    ]
    ingredients = [int(i) for i in ingredients]

    # sort ranges by start value
    ranges.sort(key=lambda r: r.start)

    newranges = []
    while ranges:
        r = ranges.pop(0)
        while ranges and overlap(r, ranges[0]):
            r = union(r, ranges[0])
            ranges.pop(0)
        newranges.append(r)

    print(sum(len(r) for r in newranges))


if __name__ == '__main__':
    part1(script_dir / 'test1.txt')
    part1(script_dir / 'input.txt')

    part2(script_dir / 'test1.txt')
    part2(script_dir / 'input.txt')
