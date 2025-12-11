# day 10

import heapq
import itertools
from collections import defaultdict
from pathlib import Path

from ..util import read_lines

script_dir = Path(__file__).resolve().parent


def parse(line: str) -> tuple[tuple[bool], list[tuple[int]], tuple[int]]:
    parts = line.split(' ')
    target = tuple(c == '#' for c in parts[0][1:-1])
    buttons = [tuple(map(int, p[1:-1].split(','))) for p in parts[1:-1]]
    joltage = tuple(map(int, parts[-1][1:-1].split(',')))
    return target, buttons, joltage


def combos(n: int, m: int):
    # all length n combos that sum to m
    for cuts in itertools.combinations(range(m + n - 1), n - 1):
        prev = -1
        parts = []
        for c in cuts + (m + n - 1,):
            parts.append(c - prev - 1)
            prev = c
        yield parts


def press_inplace(joltage, button, n):
    for b in button:
        joltage[b] -= n


def press(state, button):
    state = list(state)
    for b in button:
        state[b] = not state[b]
    return tuple(state)


def valid(joltage):
    return all(j >= 0 for j in joltage)


def dfs(joltage: tuple[int], buttons: list[tuple[int]]) -> int:
    """Strategy:
    At each level, find the joltage affected by the fewest buttons.
    Take those buttons, and iterate over all combinations that add up to the target joltage
    value. At each iteration, recurse down. Return the number of presses.
    """

    if all(j == 0 for j in joltage):
        return 0

    connections = defaultdict(list)
    for i, button in enumerate(buttons):
        for b in button:
            connections[b].append(i)

    jdx = min(connections, key=lambda c: (len(connections[c]), -joltage[c]))
    jval = joltage[jdx]
    try_buttons = connections[jdx]
    rest_buttons = None

    best = 1 << 30
    if not try_buttons:
        return best

    for combo in combos(len(try_buttons), jval):
        new_joltage = list(joltage)
        for i, n in enumerate(combo):
            press_inplace(new_joltage, buttons[try_buttons[i]], n)
            if not valid(new_joltage):
                break
        else:
            if rest_buttons is None:
                rest_buttons = [
                    b for i, b in enumerate(buttons) if i not in try_buttons
                ]
            sub = dfs(new_joltage, rest_buttons)
            best = min(best, sub + jval)

    return best


def part1(fn: Path) -> None:
    lines = read_lines(fn)

    tot = 0
    for line in lines:
        target, buttons, joltage_ = parse(line)
        n = npresses(target, buttons)
        tot += n
    print(f'Total: {tot}')


def npresses(target, buttons):
    heap = []
    heapq.heappush(heap, (0, (False,) * len(target)))
    visited = set()

    while (item := heapq.heappop(heap))[1] != target:
        dist, state = item
        if state in visited:
            continue
        visited.add(state)

        for b in buttons:
            heapq.heappush(heap, (dist + 1, press(state, b)))

    return item[0]


def part2(fn: Path) -> None:
    lines = read_lines(fn)

    tot = 0
    for line in lines:
        target_, buttons, joltage = parse(line)
        n = dfs(joltage, buttons)
        tot += n
    print(f'Total: {tot}')


if __name__ == '__main__':
    part1(script_dir / 'test1.txt')
    part1(script_dir / 'input.txt')

    part2(script_dir / 'test1.txt')
    part2(script_dir / 'input.txt')
