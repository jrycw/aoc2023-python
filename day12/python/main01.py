from itertools import groupby, product
from pathlib import Path


def line_factory(line):
    q_index = [i for i, ch in enumerate(line) if ch == "?"]
    lines = []
    for symbols in product("#.", repeat=len(q_index)):
        newline = list(line)  # create a new line list
        for idx, symbol in zip(q_index, symbols):
            newline[idx] = symbol
        lines.append(newline)
    return lines


def line_grouper(line):
    return [len(list(g)) for s, g in groupby("".join(line)) if s == "#"]


def cal_arrangements(record):
    line, spring_numbers = record
    spring_numbers = [int(n) for n in spring_numbers.split(",")]
    sum_spring_numbers = sum(spring_numbers)
    lines = [
        line for line in line_factory(line) if line.count("#") == sum_spring_numbers
    ]
    found_springs = [line_grouper(line) for line in lines]
    candidate = [
        found_spring for found_spring in found_springs if found_spring == spring_numbers
    ]
    return len(candidate)


def parse_input(file_path):
    with open(file_path) as f:
        for line in f:
            yield line.strip().split()


if __name__ == "__main__":
    # 8075
    file_path = Path(__file__).parent.parent / "data/input.txt"
    records = parse_input(file_path)
    result = sum(cal_arrangements(record) for record in records)
    print(f"{result=}")
