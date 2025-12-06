# day 06

import operator
from functools import reduce
from pathlib import Path

from ..util import read_lines

script_dir = Path(__file__).resolve().parent


def transpose(lines: list[str]) -> list[list[str]]:
    lines = [line.split() for line in lines]
    return [list(row) for row in zip(*lines)]


def transpose_chars(lines: list[str]) -> list[list[str]]:
    result = [[]]
    for column in zip(*lines):
        num = ''.join(column[:-1]).strip()
        op = column[-1]
        if op in '+*':
            result[-1].append(op)
        if num:
            result[-1].append(int(num))
        else:
            result.append([])
    return result


def part1(fn: Path) -> None:
    lines = read_lines(fn)
    transposed = transpose(lines)

    grand_total = 0
    for row in transposed:
        op = operator.add if row[-1] == '+' else operator.mul
        init = 0 if op == operator.add else 1
        grand_total += reduce(op, (int(x) for x in row[:-1]), init)
    print(grand_total)


def part2(fn: Path) -> None:
    lines = read_lines(fn)
    transposed = transpose_chars(lines)

    grand_total = 0
    for row in transposed:
        op = operator.add if row[0] == '+' else operator.mul
        init = 0 if op == operator.add else 1
        grand_total += reduce(op, (int(x) for x in row[1:]), init)
    print(grand_total)


if __name__ == '__main__':
    part1(script_dir / 'test1.txt')
    part1(script_dir / 'input.txt')

    part2(script_dir / 'test1.txt')
    part2(script_dir / 'input.txt')
