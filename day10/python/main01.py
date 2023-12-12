from enum import Enum, auto
from pathlib import Path
from typing import assert_never


class Direction(Enum):
    E = auto()
    W = auto()
    N = auto()
    S = auto()


class Point:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.marker = None

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self.x, self.y) == (other.x, other.y)
        return NotImplemented

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        cls_name = type(self).__name__
        return f"{cls_name}(x={self.x}, y={self.y}, symbol='{self.symbol}')"


class Sketch:
    def __init__(self):
        self.points = []

    def add_points(self, symbols: str):
        self.points.append(symbols)

    @property
    def max_x(self):
        return len(self.points[-1]) - 1

    @property
    def max_y(self):
        return len(self.points) - 1

    def get_adj_points(self, point: Point):
        x, y = point.x, point.y
        adj_coords = [
            (x + 1, y, Direction.E),
            (x - 1, y, Direction.W),
            (x, y + 1, Direction.S),
            (x, y - 1, Direction.N),
        ]
        adj_points = []
        for cx, cy, direction in adj_coords:
            if 0 <= cx <= self.max_x and 0 <= cy <= self.max_y:
                point = self.retrieve_point(cx, cy)
                if point.symbol in find_possible_symbols(direction):
                    adj_points.append(point)
        return adj_points

    def retrieve_point(self, x, y):
        return self.points[y][x]

    def solve(self):
        points = [self.s_point]
        round = 1
        while True:
            total_points = set()
            for point in points:
                for adj_point in self.get_adj_points(point):
                    total_points.add(adj_point)
            points = [point for point in total_points if point.marker is None]
            for pt in points:
                pt.marker = True
            if len(set(points)) == 1:
                break
            round += 1
        return round

    def __repr__(self):
        cls_name = type(self).__name__
        return f"{cls_name}(max_x={self.max_x}, max_y={self.max_y})"


def find_possible_symbols(direction):
    match direction:
        case Direction.E:
            return "-J7"
        case Direction.W:
            return "-LF"
        case Direction.S:
            return "|LJ"
        case Direction.N:
            return "|7F"
        case _:
            assert_never("Direction should be one of EWSN")


def parse_input(file_path):
    sketch = Sketch()
    with open(file_path) as f:
        for y, line in enumerate(f):
            line = line.strip()
            points = []
            for x, symbol in enumerate(line):
                point = Point(x, y, symbol)
                if symbol == "S":
                    sketch.s_point = point
                points.append(point)
            sketch.add_points(points)
    return sketch


if __name__ == "__main__":
    # 6786
    file_path = Path(__file__).parent.parent / "data/input.txt"
    sketch = parse_input(file_path)
    print(sketch.solve())
