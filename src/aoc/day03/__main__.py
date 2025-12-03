# day 03

from pathlib import Path

from ..util import read_lines

script_dir = Path(__file__).resolve().parent


def argsort(a: list[int], reverse=False) -> list[int]:
    return sorted(range(len(a)), key=lambda k: a[k], reverse=reverse)


def part1(fn: Path) -> None:
    lines = read_lines(fn)

    ans = 0
    for line in lines:
        bank = [int(i) for i in line]
        iord = argsort(bank, reverse=True)
        i1 = iord[0] if iord[0] != len(bank) - 1 else iord[1]
        ans += bank[i1] * 10
        i2 = next(filter(lambda i: i > i1, iord))
        ans += bank[i2]
        # print(f'line={line} ans={ans}')
    print(ans)


def part2(fn: Path) -> None:
    lines = read_lines(fn)

    ans = 0
    for line in lines:
        bank_ans = ''
        bank = [int(i) for i in line]
        iord = argsort(bank, reverse=True)

        i1 = -1
        for d in range(12):
            i1 = next(filter(lambda i: i < len(bank) - 11 + d and i > i1, iord))
            bank_ans += str(bank[i1])
        # print(bank_ans)
        # print(f'line={line} ans={ans}')

        ans += int(bank_ans)
    print(ans)


if __name__ == '__main__':
    part1(script_dir / 'test1.txt')
    part1(script_dir / 'input.txt')

    part2(script_dir / 'test1.txt')
    part2(script_dir / 'input.txt')
