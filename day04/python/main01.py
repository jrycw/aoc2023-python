from pathlib import Path


def cal_points(n):
    if n <= 0:
        return 0
    return 2 ** (n - 1)


def parse_input(line):
    winning_numbers, our_numbers = line.split("|")
    our_numbers = set(our_numbers.strip().split())
    winning_numbers = set(winning_numbers.split(":")[1].strip().split())
    n = len(winning_numbers) - len(winning_numbers - our_numbers)
    return cal_points(n)


def read_input(file_path):
    with open(file_path) as f:
        for line in f:
            yield parse_input(line.strip())


if __name__ == "__main__":
    # 26426
    file_path = Path(__file__).parent.parent / "data/input.txt"
    result = sum(read_input(file_path))
    print(f"{result=}")
