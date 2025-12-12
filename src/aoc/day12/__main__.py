# day 12

from pathlib import Path


script_dir = Path(__file__).resolve().parent


def parse(
    txt: str,
) -> tuple[list[frozenset[tuple[int, int]]], list[tuple[tuple[int, int], list[int]]]]:
    sections = txt.strip().split('\n\n')

    # Parse pieces (first 6 sections)
    pieces = []
    for i in range(6):
        section = sections[i]
        lines = section.split('\n')[1:]  # Skip the "N:" line
        piece_coords = set()
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == '#':
                    piece_coords.add((row, col))
        pieces.append(frozenset(piece_coords))

    # Parse puzzles
    puzzles = []
    for pz in sections[6].strip().split('\n'):
        parts = pz.split(': ')
        dims_str = parts[0]  # e.g., "4x4" or "12x5"
        piece_nums = list(map(int, parts[1].split()))

        # Parse dimensions
        height, width = map(int, dims_str.split('x'))
        puzzles.append(((height, width), piece_nums))

    return pieces, puzzles


def valid_board(dim, pieces):
    board = set()
    for piece in pieces:
        if board & piece:
            return False
        if not all(0 <= r < dim[0] and 0 <= c < dim[1] for r, c in piece):
            return False
        board |= piece
    return True


def translate(
    piece: frozenset[tuple[int, int]] | set[tuple[int, int]], dr: int, dc: int
) -> frozenset[tuple[int, int]]:
    return frozenset((r + dr, c + dc) for (r, c) in piece)


def rot90(
    piece: frozenset[tuple[int, int]] | set[tuple[int, int]],
) -> frozenset[tuple[int, int]]:
    """
    Rotate a 3x3 piece 90° clockwise "in place" in global coordinates.

    Assumes the piece occupies cells within a 3x3 block whose origin is the
    top-left (min row, min col) among its occupied cells.
    """
    min_r = min(r for r, _ in piece)
    min_c = min(c for _, c in piece)

    out: set[tuple[int, int]] = set()
    for r, c in piece:
        lr, lc = r - min_r, c - min_c  # local 0..2 (assumed)
        nr, nc = lc, 2 - lr
        out.add((min_r + nr, min_c + nc))
    return frozenset(out)


def flip(
    piece: frozenset[tuple[int, int]] | set[tuple[int, int]],
) -> frozenset[tuple[int, int]]:
    """
    Flip a 3x3 piece horizontally (mirror left-right) "in place" in global coordinates.

    Assumes the piece occupies cells within a 3x3 block whose origin is the
    top-left (min row, min col) among its occupied cells.
    """
    min_r = min(r for r, _ in piece)
    min_c = min(c for _, c in piece)

    out: set[tuple[int, int]] = set()
    for r, c in piece:
        lr, lc = r - min_r, c - min_c  # local 0..2 (assumed)
        nr, nc = lr, 2 - lc
        out.add((min_r + nr, min_c + nc))
    return frozenset(out)


def generate_next(
    pieces: tuple[frozenset[tuple[int, int]], ...],
    dim,
    visited,
):
    """Generate all possible next states by, for each piece, yielding all combos of:
    - moving one step in each direction
    - rotating 90 degrees in-place
    - flipping in-place
    """

    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for i, piece in enumerate(pieces):
        # Moves
        for dr, dc in moves:
            new_piece = translate(piece, dr, dc)
            if not all(0 <= r < dim[0] and 0 <= c < dim[1] for r, c in new_piece):
                continue
            new_state = pieces[:i] + (new_piece,) + pieces[i + 1 :]
            if new_state in visited:
                continue
            yield new_state

        # Rotation
        new_piece = rot90(piece)
        new_state = pieces[:i] + (new_piece,) + pieces[i + 1 :]
        if new_state in visited:
            continue
        yield new_state

        # Flip
        new_piece = flip(piece)
        new_state = pieces[:i] + (new_piece,) + pieces[i + 1 :]
        if new_state in visited:
            continue
        yield new_state


def has_solution(
    dim: tuple[int, int], pieces: tuple[frozenset[tuple[int, int]], ...]
) -> bool:
    queue = []
    visited = set()
    queue.append(pieces)

    while queue and (pieces := queue.pop(0)):
        if pieces in visited:
            continue
        # print(f"Visiting state with pieces: {pieces}")
        if valid_board(dim, pieces):
            return True
        visited.add(pieces)

        for next_pieces in generate_next(pieces, dim, visited):
            queue.append(next_pieces)
    return False


def has_easy_solution(
    dim: tuple[int, int], pieces: tuple[frozenset[tuple[int, int]], ...]
) -> bool:
    """Check if the board is big enough to hold all pieces in a non-overlapping manner"""
    nx = dim[0] // 3
    ny = (len(pieces) + nx - 1) // nx
    return ny * 3 <= dim[1]


def part1(fn: Path) -> None:
    pieces, puzzles = parse(open(fn).read())

    nvalid = 0
    for puzzle in puzzles:
        dim = puzzle[0]
        counts = puzzle[1]
        this_pieces = tuple(
            p for i in range(len(counts)) for p in [pieces[i]] * counts[i]
        )
        # if has_solution(dim, this_pieces):
        if has_easy_solution(dim, this_pieces):
            nvalid += 1
        print(f'Puzzle {puzzle} done')
    print(nvalid)


def part2(fn: Path) -> None:
    pieces, puzzles = parse(open(fn).read())


if __name__ == '__main__':
    part1(script_dir / 'test1.txt')
    part1(script_dir / 'input.txt')

    # part2(script_dir / 'test1.txt')
    # part2(script_dir / 'input.txt')
