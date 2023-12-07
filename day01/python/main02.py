import string
from pathlib import Path

numbers_in_eng = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]
number_map = dict(zip(numbers_in_eng, range(10))) | dict(zip(string.digits, range(10)))
reversed_number_map = {k[::-1]: v for k, v in number_map.items()}


def _parse_input(line: str, n_map: dict):
    tmp = ""
    for char in line:
        if char in n_map:
            return char
        else:
            tmp += char
            for n in range(len(tmp)):
                if (result := tmp[n:]) in n_map:
                    return result


def parse_input(line: str):
    first = number_map[_parse_input(line, number_map)]
    last = reversed_number_map[_parse_input(line[::-1], reversed_number_map)]
    return int(f"{first}{last}")


def read_input(filename: str):
    with open(filename) as f:
        for line in f:
            yield parse_input(line.strip())


if __name__ == "__main__":
    # 54019
    file_path = Path(__file__).parent.parent / "data/input.txt"
    result = sum(read_input(file_path))
    print(f"{result=}")
