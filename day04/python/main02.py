from collections import defaultdict
from pathlib import Path


def parse_input(line):
    winning_numbers, our_numbers = line.split("|")
    our_numbers = set(our_numbers.strip().split())
    winning_numbers = set(winning_numbers.split(":")[1].strip().split())
    return len(winning_numbers) - len(winning_numbers - our_numbers)


def read_input(file_path):
    with open(file_path) as f:
        for line in f:
            yield parse_input(line.strip())


if __name__ == "__main__":
    # 6227972
    pool = defaultdict(int)
    file_path = Path(__file__).parent.parent / "data/input.txt"
    n_matches = list(read_input(file_path))
    rounds = len(n_matches)
    counts = 0
    for i, n_match in zip(range(rounds), n_matches):
        i += 1  # start with round1 is much eaiser to think about
        pool[i] += 1  # add orig

        # cal orig and copies
        n_cards = pool[i]
        counts += n_cards  # add to pool
        while n_cards:
            start = i + 1
            end = start + n_match
            for j in range(start, end):
                pool[j] += 1
            n_cards -= 1
        pool[i] = 0  # consumed
    print(sum(pool.values()))
    print(counts)
