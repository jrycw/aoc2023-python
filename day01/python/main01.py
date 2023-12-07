from collections.abc import Iterator
from pathlib import Path


def get_first_and_last_digit(line: str) -> int:
    filtered = [char for char in line if char.isdigit()]
    return int(f"{filtered[0]}{filtered[-1]}")


def parse_input(file_path: str | Path) -> Iterator[int]:
    with open(file_path) as f:
        for line in f:
            yield get_first_and_last_digit(line.strip())


def cal_result(file_path: str | Path) -> int:
    return sum(parse_input(file_path))


if __name__ == "__main__":
    # 54632
    file_path = Path(__file__).parent.parent / "data/input.txt"
    result = cal_result(file_path)
    print(f"{result=}")
