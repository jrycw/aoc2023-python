from itertools import cycle
from math import lcm
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
    when_to_reach_z = []
    keys = [key for key in mapping if key.endswith("A")]
    for key in keys:
        for counts, lr in enumerate(directions, start=1):
            idx = lr_to_index(lr)
            key = mapping.get(key)[idx]
            if key.endswith("Z"):
                when_to_reach_z.append(counts)
                break
    return when_to_reach_z


def parse_input(file_path):
    mapping = {}
    with open(file_path) as f:
        directions = cycle(next(f).strip())
        next(f)  # skip empty line
        mapping = get_mapping(f)
    return directions, mapping


if __name__ == "__main__":
    # 13663968099527
    file_path = Path(__file__).parent.parent / "data/input.txt"
    directions, mapping = parse_input(file_path)
    result = lcm(*find_dest(directions, mapping))
    print(f"{result=}")
