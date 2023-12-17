from collections import defaultdict  # noqa: F401
from functools import cache
from pathlib import Path


def handle_one(mapping, s):
    if s[-1] == "-":
        label = s[:-1]
        box_number = parse_one_item(label)
        if lst := mapping[box_number]:
            mapping[box_number] = [(lbl, _) for lbl, _ in lst if label != lbl]
    else:
        label, focus_len = s.split("=")
        box_number = parse_one_item(label)
        focus_len = int(focus_len)
        info_tuple = (label, focus_len)
        lst = mapping.get(box_number, [])
        for idx, (lbl, _) in enumerate(lst):
            if label == lbl:
                mapping[box_number][idx] = info_tuple
                break
        else:
            mapping[box_number].append(info_tuple)


def handle_seq(mapping, seq):
    for s in seq:
        handle_one(mapping, s)


def hash_alg(ch, acc):
    acc += ord(ch)
    acc *= 17
    return divmod(acc, 256)[1]


@cache
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


def parse_input(file_path):
    with open(file_path) as f:
        return f.read().split(",")


def cal_result(mapping):
    result = 0
    for box_number, lst in mapping.items():
        for slot_number, (_, focus_len) in enumerate(lst, start=1):
            result += (box_number + 1) * slot_number * focus_len
    return result


if __name__ == "__main__":
    # 268497
    file_path = Path(__file__).parent.parent / "data/input.txt"
    seq = parse_input(file_path)

    mapping = defaultdict(list)
    handle_seq(mapping, seq)

    result = cal_result(mapping)
    print(f"{result=}")
