# day 02

from pathlib import Path

from ..util import read_lines

script_dir = Path(__file__).resolve().parent


def is_invalid(i: int, p2=False):
    s = str(i)

    if not p2:
        return s[: len(s) // 2] == s[len(s) // 2 :]

    for b in range(1, len(s) // 2 + 1):
        if s[:b] * (len(s) // b) == s:
            return True
    return False


def part1(fn: Path) -> None:
    lines = read_lines(fn)
    ranges = [tuple(int(i) for i in s.split('-')) for s in lines[0].split(',')]

    ans = 0
    for r in ranges:
        for i in range(r[0], r[1] + 1):
            if is_invalid(i):
                ans += i

    print(ans)


def part2(fn: Path) -> None:
    lines = read_lines(fn)
    ranges = [tuple(int(i) for i in s.split('-')) for s in lines[0].split(',')]

    ans = 0
    for r in ranges:
        for i in range(r[0], r[1] + 1):
            if is_invalid(i, True):
                ans += i

    print(ans)


if __name__ == '__main__':
    part1(script_dir / 'test1.txt')
    part1(script_dir / 'input.txt')

    part2(script_dir / 'test1.txt')
    part2(script_dir / 'input.txt')
