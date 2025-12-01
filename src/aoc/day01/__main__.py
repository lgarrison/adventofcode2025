# day 01

from pathlib import Path

from ..util import read_lines

script_dir = Path(__file__).resolve().parent


def part1(fn: Path) -> None:
    lines = read_lines(fn)

    dial = 50
    zcount = 0
    for line in lines:
        dial += (-1 if line[0] == 'L' else 1) * int(line[1:])
        dial %= 100
        if dial == 0:
            zcount += 1

    print(f'{fn.name}: {zcount}')


def part2(fn: Path) -> None:
    lines = read_lines(fn)

    dial = 50
    zcount = 0
    left = False
    for line in lines:
        if (line[0] == 'L') != left:
            dial = (100 - dial) % 100
            left = not left

        dial = dial + int(line[1:])
        zcount += dial // 100
        dial %= 100

    print(f'{fn.name}: {zcount}')


if __name__ == '__main__':
    part1(script_dir / 'test1.txt')
    part1(script_dir / 'input.txt')

    part2(script_dir / 'test1.txt')
    part2(script_dir / 'input.txt')
