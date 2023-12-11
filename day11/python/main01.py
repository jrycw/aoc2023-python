from copy import deepcopy
from itertools import combinations
from pathlib import Path


class Image:
    def __init__(self):
        self._unis = []

    def add_line(self, line):
        self._unis.append(line)

    def _expand(self):
        ys = [i for i, line in enumerate(self._unis) if "#" not in line]
        xs = [i for i, line in enumerate(zip(*self._unis)) if "#" not in line]
        len_x = len(self._unis[-1])
        for y in reversed(ys):
            self._unis.insert(y, "." * len_x)

        for x in reversed(xs):
            unis = deepcopy(self._unis)
            for i, line in enumerate(unis):
                self._unis[i] = line[:x] + "." + line[x:]

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


def cal_dist(comb):
    (x1, y1), (x2, y2) = comb
    return abs(x1 - x2) + abs(y1 - y2)


if __name__ == "__main__":
    file_path = Path(__file__).parent.parent / "data/sample01.txt"
    image = parse_input(file_path)
    print("original: ")
    for line in image:
        print(line)
    image._expand()
    print("expanding: ")
    for line in image:
        print(line)

    galaxy_coords = image.get_galaxy_coords()
    combs = list(combinations(galaxy_coords, 2))
    result = sum(cal_dist(comb) for comb in combs)
    print(f"{result=}")
