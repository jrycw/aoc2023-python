from itertools import cycle
from pathlib import Path
from typing import assert_never


def get_mapping(f):
    mapping = {}
    for line in f:
        key, _value = line.strip().split("=")
        value = _value.strip().removeprefix("(").removesuffix(")").split(",")
        key = key.strip()
        value = [v.strip() for v in value]
        mapping[key] = value
    return mapping


def lr_to_index(lr):
    match lr:
        case "L":
            return 0
        case "R":
            return 1
        case _:
            assert_never()


def find_dest(directions, mapping):
    active_key, last_key = "AAA", "ZZZ"
    for counts, lr in enumerate(directions, start=1):
        idx = lr_to_index(lr)
        active_key = mapping.get(active_key)[idx]
        if active_key == last_key:
            return counts


def parse_input(file_path):
    mapping = {}
    with open(file_path) as f:
        directions = cycle(next(f).strip())
        next(f)  # skip empty line
        mapping = get_mapping(f)
    return directions, mapping


if __name__ == "__main__":
    # 19199
    file_path = Path(__file__).parent.parent / "data/input.txt"
    directions, mapping = parse_input(file_path)
    result = find_dest(directions, mapping)
    print(f"{result=}")
