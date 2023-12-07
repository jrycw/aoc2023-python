from pathlib import Path


def parse_input(line: str):
    gid, row = line.split(":")
    gid = int(gid.removeprefix("Game "))
    for group in row.split(";"):
        d = dict()
        for item in group.split(","):
            v, k = item.split()
            d[k] = int(v)
        r = d.get("red", 0)
        g = d.get("green", 0)
        b = d.get("blue", 0)
        if r > 12 or g > 13 or b > 14:
            return 0
    return gid


def read_input(filename):
    with open(filename) as f:
        for line in f:
            yield parse_input(line.strip())


if __name__ == "__main__":
    # 2237
    file_path = Path(__file__).parent.parent / "data/input.txt"
    result = sum(read_input(file_path))
    print(f"{result=}")
