# day 04

from pathlib import Path

from ..util import read_lines

script_dir = Path(__file__).resolve().parent


def count_adj(grid, loc: tuple[int, int]) -> int:
    DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    result = []
    for dx, dy in DIRS:
        if (loc[0] + dx, loc[1] + dy) in grid:
            result.append((loc[0] + dx, loc[1] + dy))
    return len(result)


def part1(fn: Path) -> None:
    lines = read_lines(fn)

    grid = {}
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch == '@':
                grid[(r, c)] = ch

    ans = 0
    for loc in grid:
        n = count_adj(grid, loc)
        if n < 4:
            ans += 1
    print(ans)


def part2(fn: Path) -> None:
    lines = read_lines(fn)

    grid = {}
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch == '@':
                grid[(r, c)] = ch

    done = False
    ans = 0
    while not done:
        done = True
        for loc in dict(grid):
            n = count_adj(grid, loc)
            if n < 4:
                grid.pop(loc)
                ans += 1
                done = False
    print(ans)


if __name__ == '__main__':
    part1(script_dir / 'test1.txt')
    part1(script_dir / 'input.txt')

    part2(script_dir / 'test1.txt')
    part2(script_dir / 'input.txt')
