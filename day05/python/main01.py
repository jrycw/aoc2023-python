from itertools import groupby
from pathlib import Path


class Table:
    def __init__(self):
        self.mappping = {}

    def parse_group(self, group):
        map_name, *infos = map(str.strip, group)
        keys, values = [], []
        for info in infos:
            dest, src, range_len = [int(item) for item in info.strip().split()]
            key = range(src, src + range_len)  # seed
            keys.append(key)
            value = range(dest, dest + range_len)  # soil
            values.append(value)
        self.mappping[map_name] = dict(zip(keys, values))

    def parse_seed(self, seed_n):
        for map_name in self.mappping:
            seed_n = self.parse_mapping(seed_n, map_name)
        return seed_n

    def parse_mapping(self, seed_n: int, map_name: str):
        for key, value in self.mappping[map_name].items():
            if seed_n in key:
                idx = key.index(seed_n)
                return value[idx]
        return seed_n


def parse_input(file_path):
    with open(file_path) as f:
        seed_numbers = list(map(int, next(f).strip().split(":")[-1].split()))
        groups = [
            list(g) for k, g in groupby(f, key=lambda line: line == "\n") if not k
        ]
        table = Table()
        for group in groups:
            table.parse_group(group)
        return [table.parse_seed(seed_n) for seed_n in seed_numbers]


if __name__ == "__main__":
    # 88151870
    file_path = Path(__file__).parent.parent / "data/input.txt"
    converted = parse_input(file_path)
    print(f"{converted=}")
    result = min(converted)
    print(f"{result=}")
