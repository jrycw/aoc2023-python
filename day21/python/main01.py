from functools import cache
from pathlib import Path

"""
grid direction
+x => +x
-y => +y
"""

markers = {"starting": "S", "rock": "#", "gplot": "."}


def parse_input(file_path):
    with open(file_path) as f:
        return f.read().splitlines()


def locate_s(grid):
    for y, line in enumerate(grid):
        for x, ch in enumerate(line):
            if ch == markers["starting"]:
                return x, y


def locate_rocks(grid):
    rocks = set()
    for y, line in enumerate(grid):
        for x, ch in enumerate(line):
            if ch == markers["rock"]:
                rocks.add((x, y))
    return rocks


@cache
def get_directions(s_point):
    x, y = s_point
    up = x, y - 1
    down = x, y + 1
    left = x + 1, y
    right = x - 1, y
    directions = [up, down, left, right]
    return [
        (_x, _y)
        for _x, _y in directions
        if (0 <= _x < max_x and 0 <= _y < max_y and ((_x, _y) not in rocks))
    ]


def square_search(grid, s_point):
    x, y = s_point
    grid[y][x] = markers["gplot"]  # grid is mutated
    directions = get_directions(s_point)

    s_points = []
    for _x, _y in directions:
        s_points.append((_x, _y))
        grid[_y][_x] = markers["starting"]  # grid is mutated
    return grid, s_points


def one_move(grid, s_points):
    points = set()
    for s_point in s_points:
        grid, cur_pts = square_search(grid, s_point)
        points.update(cur_pts)
    return grid, points


def display_grid(grid):
    print("\n".join("".join(line) for line in grid), end="\n" * 2)


def cal_result(grid):
    return sum(1 for line in grid for ch in line if ch == markers["starting"])


if __name__ == "__main__":
    # 3598
    file_path = Path(__file__).parent.parent / "data/input.txt"
    grid = parse_input(file_path)
    grid = [list(line) for line in grid]

    max_x = len(grid[0])
    max_y = len(grid)
    s_points = [locate_s(grid)]
    rocks = locate_rocks(grid)

    n_step = 64
    for i in range(n_step):
        grid, s_points = one_move(grid, s_points)
    display_grid(grid)

    result = cal_result(grid)
    print(f"{result=}")
