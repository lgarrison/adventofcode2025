# day 07

import functools
from collections import defaultdict
from pathlib import Path

from ..util import read_lines

script_dir = Path(__file__).resolve().parent


def parse_diagram(
    lines: list[str],
) -> tuple[tuple[int, int], int, set[tuple[int, int]]]:
    grid: set[tuple[int, int]] = set()

    start = None
    end = 0
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == '^':
                grid.add((x, y))
                end = max(end, y)
            if ch == 'S':
                start = (x, y)

    return start, end + 1, grid


def build_tree(start, end, grid) -> dict[tuple[int, int], set[tuple[int, int]]]:
    queue = [(start, start)]
    visited = set()
    tree = defaultdict(set)

    while queue:
        parent, beam = queue.pop()
        x, y = beam
        while y < end:
            y += 1
            if (x, y) in grid:
                tree[parent].add((x, y))
                if (x, y) in visited:
                    break
                visited.add((x, y))
                queue.append(((x, y), (x - 1, y)))
                queue.append(((x, y), (x + 1, y)))
                break
        else:
            tree[parent].add((x, end))

    return dict(tree)


def count_paths(start: tuple[int, int], tree) -> int:
    @functools.lru_cache()
    def count_paths_(start: tuple[int, int]):
        # print(f'count_paths({start})')
        return sum(count_paths_(child) for child in tree[start]) if start in tree else 1

    return count_paths_(start)


def part1(fn: Path) -> None:
    lines = read_lines(fn)
    start, end, grid = parse_diagram(lines)
    tree = build_tree(start, end, grid)
    print(len(tree.keys()) - 1)


def part2(fn: Path) -> None:
    lines = read_lines(fn)
    start, end, grid = parse_diagram(lines)
    tree = build_tree(start, end, grid)
    print(count_paths(start, tree))


if __name__ == '__main__':
    part1(script_dir / 'test1.txt')
    part1(script_dir / 'input.txt')

    part2(script_dir / 'test1.txt')
    part2(script_dir / 'input.txt')
