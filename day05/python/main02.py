from itertools import groupby
from pathlib import Path


class Table:
    def __init__(self):
        self.mapping = {}
        self._reversed_sorted_mapping = {}
        self.map_names = []
        self._reversed_map_names = []

    def parse_group(self, group):
        map_name, *infos = map(str.strip, group)
        self.map_names.append(map_name)
        keys, values = [], []
        for info in infos:
            dest, src, range_len = [int(item) for item in info.strip().split()]
            key = range(src, src + range_len)  # seed
            keys.append(key)
            value = range(dest, dest + range_len)  # soil
            values.append(value)
        self.mapping[map_name] = dict(zip(keys, values))
        return self.mapping[map_name]

    @property
    def reversed_sorted_mapping(self):
        if not self._reversed_sorted_mapping:
            for map_name in self.map_names:
                mapping = {v: k for k, v in self.mapping[map_name].items()}
                self._reversed_sorted_mapping[map_name] = dict(
                    sorted(mapping.items(), key=lambda t: t[0].start)
                )
        return self._reversed_sorted_mapping

    @property
    def reversed_map_names(self):
        if not self._reversed_map_names:
            self._reversed_map_names = list(reversed(self.map_names))
        return self._reversed_map_names

    def parse_seed(self, seed_n):
        for map_name in self.map_names:
            seed_n = self.parse_mapping(seed_n, map_name)
        return seed_n

    def parse_loc(self, loc):
        for map_name in reversed(self.map_names):
            loc = self.parse_reversed_mapping(loc, map_name)
        return loc

    def parse_mapping(self, seed_n: int, map_name: str):
        for key, value in self.mapping[map_name].items():
            if seed_n in key:
                idx = key.index(seed_n)
                return value[idx]
        return seed_n

    def parse_reversed_mapping(self, loc: int, map_name: str):
        mapping = self.reversed_sorted_mapping[map_name]
        for key, value in mapping.items():
            if loc in key:
                idx = key.index(loc)
                return value[idx]
        return loc


def group_by_2(seeds):
    it = iter(seeds)
    while True:
        try:
            yield next(it), next(it)
        except StopIteration:
            break


def get_potential(table, loc_ranges, seed_ranges):
    for loc_range in loc_ranges:
        print(f"running {loc_range=}")
        for loc in loc_range:
            parsed = table.parse_loc(loc)
            for seed_range in seed_ranges:
                if parsed in seed_range:
                    return loc


def get_loc(table, loc_ranges, seed_ranges):
    pot_loc = get_potential(table, loc_ranges, seed_ranges)
    print(f"potential loc: {pot_loc}")
    for loc in range(pot_loc):
        pot_loc2 = table.parse_loc(loc)
        for seed_range in seed_ranges:
            if pot_loc2 in seed_range:
                pot_loc = min(pot_loc, loc)
    return pot_loc


def parse_input(file_path):
    with open(file_path) as f:
        seed_pairs = list(group_by_2(map(int, next(f).strip().split(":")[-1].split())))
        print(f"{seed_pairs}")
        groups = [
            list(g) for k, g in groupby(f, key=lambda line: line == "\n") if not k
        ]
        table = Table()
        for group in groups:
            table.parse_group(group)

        seed_ranges = [
            range(start, start + len_range) for start, len_range in seed_pairs
        ]
        loc_ranges = list(
            table.reversed_sorted_mapping[table.reversed_map_names[0]].keys()
        )

        return get_loc(table, loc_ranges, seed_ranges)


if __name__ == "__main__":
    # 2008785
    # buggy?
    file_path = Path(__file__).parent.parent / "data/input.txt"
    result = parse_input(file_path)
    print(f"{result=}")
