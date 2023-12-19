from collections import defaultdict
from pathlib import Path


def parse_rules(lines):
    rules = defaultdict(dict)
    for line in lines:
        wk_name, others = line.strip("}").split("{")
        for cond in others.split(","):
            cond = cond.strip()
            if "A" == cond:
                key, value = "A", "A"
            elif "R" == cond:
                key, value = "R", "R"
            elif ":" not in cond:
                key, value = cond, cond
            else:
                key, value = cond.split(":")
            rules[wk_name][key] = value
    return dict(rules)


def parse_ratings(lines):
    ratings = []
    for line in lines:
        conds = line.strip("{}").split(",")
        d = {}
        for cond in conds:
            key, value = cond.split("=")
            d[key] = int(value)
        ratings.append(d)
    return ratings


def parse_input(file_path):
    with open(file_path) as f:
        rules, ratings = f.read().split("\n\n")
        return parse_rules(rules.splitlines()), parse_ratings(ratings.splitlines())


def get_next_key(rating, cur_rule):
    next_rule = None
    for ri_key, ri_value in cur_rule.items():
        if "<" in ri_key or ">" in ri_key:
            variable = ri_key[0]
            symbol = ri_key[1]
            rule_value = int(ri_key[2:])
            rating_value = rating.get(variable)
            match symbol:
                case "<":
                    cond = rating_value < rule_value
                case ">":
                    cond = rating_value > rule_value
            if cond:
                next_rule = ri_value
                break
    if next_rule is None:
        next_rule = ri_value
    return next_rule


def get_idxes(rules, ratings):
    rule_in = rules["in"]
    cur_rule = rule_in
    idxes = []
    for idx, cur_rating in enumerate(ratings):
        while True:
            next_key = get_next_key(cur_rating, cur_rule)
            if next_key == "A":
                idxes.append(idx)
                cur_rule = rule_in
                break
            elif next_key == "R":
                cur_rule = rule_in
                break
            else:
                cur_rule = rules[next_key]
    return idxes


def cal_result(ratings, idxes):
    return sum(sum(ratings[idx].values()) for idx in idxes)


if __name__ == "__main__":
    # 487623
    file_path = Path(__file__).parent.parent / "data/input.txt"
    rules, ratings = parse_input(file_path)
    idxes = get_idxes(rules, ratings)
    result = cal_result(ratings, idxes)
    print(f"{result=}")
