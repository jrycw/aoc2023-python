import operator
from functools import reduce
from pathlib import Path


def parse_input(line: str):
    gid, row = line.split(":")
    gid = int(gid.strip().removeprefix("Game "))

    keys = ("red", "green", "blue")
    d = dict.fromkeys(keys, 0)

    for group in row.split(";"):
        for item in group.split(","):
            v, k = item.split()
            v = int(v)
            if v > d.get(k, 0):
                d[k] = v
    return reduce(operator.mul, d.values())


def read_input(filename):
    with open(filename) as f:
        for line in f:
            yield parse_input(line.strip())


if __name__ == "__main__":
    # 66681
    file_path = Path(__file__).parent.parent / "data/input.txt"
    result = sum(read_input(file_path))
    print(f"{result=}")
