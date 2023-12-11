from itertools import pairwise
from pathlib import Path


def recover_line(first_numner):
    for i, number in enumerate(reversed(first_numner)):
        if i == 0:
            elem = number
        else:
            elem = number - elem
    return elem


def parse_line(line):
    first_numbers = []
    numbers = [int(elem) for elem in line.split()]
    while not all(number == 0 for number in numbers):
        tmp_numbers = []
        first_numbers.append(numbers[0])
        for a, b in pairwise(numbers):
            tmp_numbers.append(b - a)
        numbers = tmp_numbers
    return recover_line(first_numbers)


def parse_input(file_path):
    with open(file_path) as f:
        for line in f:
            yield parse_line(line.strip())


if __name__ == "__main__":
    # 1152
    file_path = Path(__file__).parent.parent / "data/input.txt"
    result = sum(parse_input(file_path))
    print(f"{result=}")
