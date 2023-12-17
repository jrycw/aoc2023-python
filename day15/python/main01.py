from pathlib import Path


def hash_alg(ch, acc):
    acc += ord(ch)
    acc *= 17
    _, value = divmod(acc, 256)
    return value


def parse_one_item(s):
    s = iter(s)
    value = 0
    while True:
        try:
            ch = next(s)
        except StopIteration:
            break
        else:
            value = hash_alg(ch, value)
    return value


def parse_seq(seq):
    return sum(parse_one_item(s) for s in seq)


def parse_input(file_path):
    with open(file_path) as f:
        return f.read().split(",")


if __name__ == "__main__":
    # 510013
    file_path = Path(__file__).parent.parent / "data/input.txt"
    seq = parse_input(file_path)
    result = parse_seq(seq)
    print(f"{result=}")
