from itertools import combinations
from pathlib import Path


class Image:
    def __init__(self):
        self._unis = []

    def add_line(self, line):
        self._unis.append(line)

    def get_xs_ys(self):
        ys = [i for i, line in enumerate(self._unis) if "#" not in line]
        xs = [i for i, line in enumerate(zip(*self._unis)) if "#" not in line]
        return xs, ys

    def get_galaxy_coords(self):
        return [
            (x, y)
            for y, line in enumerate(self._unis)
            for x, char in enumerate(line)
            if char == "#"
        ]

    def __iter__(self):
        return iter(self._unis)


def parse_input(file_path):
    image = Image()
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            image.add_line(line)
    return image


def cal_dist(comb, xs, ys, n):
    (x1, y1), (x2, y2) = comb
    new_x1 = min(x1, x2)
    new_x2 = max(x1, x2)
    new_y1 = min(y1, y2)
    new_y2 = max(y1, y2)

    accum, cx, cy = 0, 0, 0
    for x in xs:
        if x in range(new_x1, new_x2):
            cx += 1
    accum += cx * n

    for y in ys:
        if y in range(new_y1, new_y2):
            cy += 1
    accum += cy * n

    return abs(x1 - x2) + abs(y1 - y2) + accum


if __name__ == "__main__":
    # 447073334102
    file_path = Path(__file__).parent.parent / "data/input.txt"
    image = parse_input(file_path)
    xs, ys = image.get_xs_ys()

    galaxy_coords = image.get_galaxy_coords()
    n = 1000_000 - 1
    result = sum(cal_dist(comb, xs, ys, n) for comb in combinations(galaxy_coords, 2))
    print(f"{result=}")
