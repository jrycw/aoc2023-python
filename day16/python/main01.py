from enum import Enum, auto
from pathlib import Path
from typing import assert_never


class Arrow(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Beam:
    grid = None

    def __init__(self, x, y, arrow):
        self.x = x
        self.y = y
        self.arrow = arrow

    @property
    def max_x(self):
        return len(self.grid)

    @property
    def max_y(self):
        return len(grid[0])

    def get_next(self):
        x, y = self.x, self.y
        match self.arrow:
            case Arrow.UP:
                x -= 1
            case Arrow.DOWN:
                x += 1
            case Arrow.LEFT:
                y -= 1
            case Arrow.RIGHT:
                y += 1
            case _:
                assert_never("Impossible arrow direction")

        if not (0 <= x < self.max_x and 0 <= y < self.max_y):
            return []

        next_symbol = self.grid[x][y]
        match next_symbol:
            case ".":
                next_arrow = self.arrow
            case "/":
                match self.arrow:
                    case Arrow.UP:
                        next_arrow = Arrow.RIGHT
                    case Arrow.DOWN:
                        next_arrow = Arrow.LEFT
                    case Arrow.LEFT:
                        next_arrow = Arrow.DOWN
                    case Arrow.RIGHT:
                        next_arrow = Arrow.UP
            case "\\":
                match self.arrow:
                    case Arrow.UP:
                        next_arrow = Arrow.LEFT
                    case Arrow.DOWN:
                        next_arrow = Arrow.RIGHT
                    case Arrow.LEFT:
                        next_arrow = Arrow.UP
                    case Arrow.RIGHT:
                        next_arrow = Arrow.DOWN
            case "|":
                match self.arrow:
                    case Arrow.UP | Arrow.DOWN:
                        next_arrow = self.arrow
                    case Arrow.LEFT | Arrow.RIGHT:
                        next_arrow = [Arrow.UP, Arrow.DOWN]
            case "-":
                match self.arrow:
                    case Arrow.UP | Arrow.DOWN:
                        next_arrow = [Arrow.LEFT, Arrow.RIGHT]
                    case Arrow.LEFT | Arrow.RIGHT:
                        next_arrow = self.arrow

        try:
            arrow_iters = iter(next_arrow)
        except TypeError:
            return [Beam(x, y, next_arrow)]
        else:
            return [Beam(x, y, one_next_arrow) for one_next_arrow in arrow_iters]

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.x, self.y, self.arrow == other.x, other.y, other.arrow
        return NotImplemented

    def __hash__(self):
        return hash((self.x, self.y, self.arrow))

    def __repr__(self):
        cls_name = type(self).__name__
        return f"{cls_name}(x={self.x}, y={self.y} arrow={self.arrow})"


def get_first_arrow(grid):
    symbol = grid[0][0]
    match symbol:
        case "." | "-":
            arrow = Arrow.RIGHT
        case "\\" | "|":
            arrow = Arrow.DOWN
        case _:
            assert_never("Initially can only go right or down")
    return arrow


def run(records, first_arrow):
    total_paths = set()
    start_beam = Beam(0, 0, first_arrow)
    records.add(start_beam)
    total_paths.add((start_beam.x, start_beam.y))

    n = 1
    acc = 0
    cur_max = len(total_paths)
    while True:
        removed, added = set(), set()
        lrecords = list(records)
        for beam in lrecords:
            beam_iterables = beam.get_next()

            for one_beam in beam_iterables:
                added.add(one_beam)
            removed.add(beam)

        for one_beam in added:
            records.add(one_beam)
            total_paths.add((one_beam.x, one_beam.y))

        for one_beam in removed:
            try:
                records.remove(one_beam)
            except KeyError:
                pass

        print(f"{n=}")
        print(f"{len(total_paths)=}")
        if len(total_paths) > cur_max:
            cur_max = len(total_paths)
        else:
            acc += 1
        if acc > 50:
            return cur_max
        n += 1


def parse_input(file_path):
    with open(file_path) as f:
        return f.read().splitlines()


if __name__ == "__main__":
    # 6921
    file_path = Path(__file__).parent.parent / "data/input.txt"
    grid = tuple(parse_input(file_path))
    Beam.grid = grid
    records = set()
    first_arrow = get_first_arrow(grid)
    result = run(records, first_arrow)
    print(f"{result=}")
