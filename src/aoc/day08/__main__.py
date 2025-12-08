# day 08

from functools import reduce
from pathlib import Path

from ..util import read_lines

script_dir = Path(__file__).resolve().parent


def argsort2d(matrix: list[list[int]]) -> list[tuple[int, int]]:
    indices: list[tuple[int, int]] = []
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            indices.append((i, j))
    indices.sort(key=lambda ij: matrix[ij[0]][ij[1]])
    return indices


def pair_dists2(junctions: list[tuple[int, int, int]]) -> list[list[int]]:
    dists: list[list[int]] = []
    for i, (x1, y1, z1) in enumerate(junctions):
        row: list[int] = []
        for j, (x2, y2, z2) in enumerate(junctions):
            dist = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
            row.append(dist)
        dists.append(row)
    return dists


def find(i, circuts):
    for c in circuts:
        if i in c:
            return c
    raise ValueError(i)


def part1(fn: Path, nconnect: int) -> None:
    lines = read_lines(fn)

    junctions: list[tuple[int, int, int]] = [eval(line) for line in lines]
    # print(junctions)

    circuits = [set([i]) for i in range(len(junctions))]

    dists = pair_dists2(junctions)
    iord = argsort2d(dists)
    iord = iord[len(junctions) :][::2]  # self-distances

    for i, j in iord[:nconnect]:
        icirc = find(i, circuits)
        jcirc = find(j, circuits)

        if icirc is not jcirc:
            icirc |= jcirc
            jcirc.clear()

    print(
        reduce(
            lambda a, b: a * b, sorted([len(c) for c in circuits], reverse=True)[:3], 1
        )
    )


def part2(fn: Path) -> None:
    lines = read_lines(fn)

    junctions: list[tuple[int, int, int]] = [eval(line) for line in lines]
    # print(junctions)

    circuits = [set([i]) for i in range(len(junctions))]

    dists = pair_dists2(junctions)
    iord = argsort2d(dists)
    iord = iord[len(junctions) :][::2]  # self-distances

    for i, j in iord:
        icirc = find(i, circuits)
        jcirc = find(j, circuits)

        if icirc is not jcirc:
            icirc |= jcirc
            jcirc.clear()

        if sum(bool(c) for c in circuits) == 1:
            break
    print(junctions[i][0] * junctions[j][0])


if __name__ == '__main__':
    part1(script_dir / 'test1.txt', 10)
    part1(script_dir / 'input.txt', 1000)

    part2(script_dir / 'test1.txt')
    part2(script_dir / 'input.txt')
