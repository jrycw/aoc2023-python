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


def move_north(grid):
    grid = [list(t) for t in grid]
    return one_move(grid)


def move_south(grid):
    grid = [list(t) for t in reversed(grid)]
    grid = one_move(grid)
    return grid[::-1]


def move_west(grid):
    grid = [list(reversed(z)) for z in zip(*grid)]
    grid = one_move(grid)
    return list(zip(*[lst[::-1] for lst in grid]))


def move_east(grid):
    grid = list(zip(*grid))[::-1]
    grid = [list(z) for z in grid]
    grid = one_move(grid)
    return [lst[::-1] for lst in zip(*grid)]


def display_grid(grid):
    for g in grid:
        print("".join(g))
    print("\n")


def run_dir_func(grid, dir_func):
    while True:
        copied = deepcopy(grid)
        grid = dir_func(grid)  # grid is mutated
        if copied == grid:
            break
    return grid


def move_cycle(grid):
    dir_funcs = [move_north, move_west, move_south, move_east]
    for dir_func in dir_funcs:
        grid = run_dir_func(grid, dir_func)
    return grid


def cal_total_load(grid):
    total = 0
    len_grid = len(grid)
    for line, pt in zip(grid, range(len_grid, 0, -1)):
        total += (line.count("O")) * pt
    return total


if __name__ == "__main__":
    # 98029
    file_path = Path(__file__).parent.parent / "data/input.txt"
    grid = parse_input(file_path)

    # by observing the numbers to conclude the rules
    # (1000000000-121) - (38461533*26) = 21
    n = 200
    for i in range(n):
        grid = move_cycle(grid)
        result = cal_total_load(grid)
        print(f"{i:<10}: {result=}")
