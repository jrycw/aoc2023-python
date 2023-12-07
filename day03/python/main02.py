import operator
import re
from functools import total_ordering
from pathlib import Path


@total_ordering
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self.x, self.y) == (other.x, other.y)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.x == other.x and self.y < other.y
        return NotImplemented

    def __hash__(self):
        return hash((self.x, self.y))

    def bounds(self):
        cls = type(self)
        return [
            cls(self.x + 1, self.y),
            cls(self.x + 1, self.y + 1),
            cls(self.x, self.y + 1),
            cls(self.x - 1, self.y + 1),
            cls(self.x - 1, self.y),
            cls(self.x - 1, self.y - 1),
            cls(self.x, self.y - 1),
            cls(self.x + 1, self.y - 1),
        ]

    def __repr__(self):
        cls_name = type(self).__name__
        return f"{cls_name}({self.x}, {self.y})"


class Box:
    __slots__ = ("p1", "p2", "value")

    def __init__(self, x, y1, y2, value):
        self.p1 = Point(x, y1)
        self.p2 = Point(x, y2)
        self.value = value

    def __contains__(self, other):
        if isinstance(other, Point):
            return any(self.p1 <= pt <= self.p2 for pt in other.bounds())
        return NotImplemented

    def __repr__(self):
        cls_name = type(self).__name__
        return f"{cls_name}(p1={self.p1}, p2={self.p2}, value={self.value})"


def read_input(file_path):
    with open(file_path) as f:
        for i, line in enumerate(f):
            yield (i, line.strip())


def find_symbol_yloc(line):
    symbols = re.finditer(r"[^\d\.]", line)
    return [symbol.start() for symbol in symbols]


def find_box_ybound_and_value(line: str) -> int:
    result = []
    digits = re.finditer(r"(\d+)?", line)
    for digit in digits:
        if v := digit.group():
            y1 = digit.start()
            y2 = digit.end() - 1
            result.append((y1, y2, int(v)))
    return result


if __name__ == "__main__":
    # 83279367
    file_path = Path(__file__).parent.parent / "data/input.txt"
    points, boxes, gears = [], [], []

    for i, line in read_input(file_path):
        if ylocs := find_symbol_yloc(line):
            for yloc in ylocs:
                points.append(Point(i, yloc))
        if b_ylocs_value := find_box_ybound_and_value(line):
            for b_yloc_value in b_ylocs_value:
                boxes.append(Box(i, *b_yloc_value))

    # assume exactly two part numbers, no more than two
    for pt in points:
        gear = []
        for box in boxes:
            if pt in box:
                gear.append(box.value)
                if len(gear) <= 1:
                    continue
                gears.append(gear)
                break

    result = sum(operator.mul(*g) for g in gears)
    print(f"{result=}")
