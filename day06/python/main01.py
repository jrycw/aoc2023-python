from pathlib import Path


def get_info(t, dist):
    win_ways = 0
    for i in range(t + 1):
        v = i
        remained_time = t - i
        distance = v * remained_time
        if distance > dist:
            win_ways += 1
    return win_ways


def parse_input(file_path):
    with open(file_path) as f:
        times = next(f).strip().split(":")[-1].split()
        distance = next(f).strip().split(":")[-1].split()
        times = [int(t) for t in times]
        distance = [int(dist) for dist in distance]
        return times, distance


if __name__ == "__main__":
    # 293046
    file_path = Path(__file__).parent.parent / "data/input.txt"
    result = 1
    for t, dist in zip(*parse_input(file_path)):
        result *= get_info(t, dist)
    print(result)
