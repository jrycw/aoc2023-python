from copy import deepcopy
from pathlib import Path


def parse_input(file_path):
    with open(file_path) as f:
        return [
            list(line) for line in f.read().splitlines()
        ]  # list(line) for easily index later


def one_move(grid):
    iter_grid = deepcopy(grid)
    for line_idx, line in enumerate(iter_grid):
        if line_idx == 0:
            continue
        for e_idx, elem in enumerate(line):
            hole = grid[line_idx - 1][e_idx]
            if elem == "O" and hole == ".":
                grid[line_idx - 1][e_idx] = "O"
                grid[line_idx][e_idx] = "."
    return grid


def run(grid):
    while True:
        copied = deepcopy(grid)
        one_move(grid)  # grid is mutated
        if copied == grid:
            break
    return grid


def display_grid(grid):
    for g in grid:
        print("".join(g))
    print("\n")


def cal_total_load(grid):
    total = 0
    len_grid = len(grid)
    for line, pt in zip(grid, range(len_grid, 0, -1)):
        total += (line.count("O")) * pt
    return total


if __name__ == "__main__":
    # 105623
    file_path = Path(__file__).parent.parent / "data/input.txt"
    grid = parse_input(file_path)
    grid = run(grid)
    display_grid(grid)
    result = cal_total_load(grid)
    print(f"{result=}")
