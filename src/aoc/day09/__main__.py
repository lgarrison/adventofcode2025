# day 09

from pathlib import Path

from ..util import read_lines

script_dir = Path(__file__).resolve().parent


def adist(a: tuple[int, int], b: tuple[int, int]) -> int:
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


def segment_intersects_rect(
    seg: tuple[tuple[int, int], tuple[int, int]],
    rect_corners: tuple[tuple[int, int], tuple[int, int]],
) -> bool:
    """check if a segment intersects a rectangle by checking if
    it falls completely above, below, to the right, or to the left.
    """

    (x1, y1), (x2, y2) = seg
    (rx1, ry1), (rx2, ry2) = rect_corners

    min_rx, max_rx = min(rx1, rx2), max(rx1, rx2)
    min_ry, max_ry = min(ry1, ry2), max(ry1, ry2)

    if max(x1, x2) <= min_rx:
        return False
    if min(x1, x2) >= max_rx:
        return False
    if min(y1, y2) >= max_ry:
        return False
    if max(y1, y2) <= min_ry:
        return False

    return True


def part1(fn: Path) -> None:
    lines = read_lines(fn)

    coords = [tuple(map(int, line.split(','))) for line in lines]

    print(max(adist(c1, c2) for c1 in coords for c2 in coords))


def part2(fn: Path) -> None:
    lines = read_lines(fn)

    coords = [tuple(map(int, line.split(','))) for line in lines]
    line_segments = list(zip(coords, coords[1:] + [coords[0]]))

    max_area = 0
    max_corners = None
    for corner1 in coords:
        for corner2 in coords:
            if corner1 == corner2:
                continue
            for seg in line_segments:
                if segment_intersects_rect(seg, (corner1, corner2)):
                    break
            else:
                area = adist(corner1, corner2)
                # print(f"Found rectangle between {corner1} and {corner2} with area {area}")
                if area > max_area:
                    max_area = area
                    max_corners = (corner1, corner2)
    print(f'Max area found: {max_area} with corners {max_corners}')


if __name__ == '__main__':
    part1(script_dir / 'test1.txt')
    part1(script_dir / 'input.txt')

    part2(script_dir / 'test1.txt')
    part2(script_dir / 'input.txt')
