from collections import Counter
from enum import IntEnum, auto
from functools import total_ordering
from pathlib import Path


class CardLabelStrength(IntEnum):
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    T = auto()
    J = auto()
    Q = auto()
    K = auto()
    A = auto()


label_mapping = CardLabelStrength.__members__
label_str_mapping = dict(
    zip(
        list("23456789TJQKA"),
        label_mapping.keys(),
    )
)


def get_label_enum(label):
    return label_mapping.get(label_str_mapping.get(label))


class HandStrength(IntEnum):
    HIGHCARD = auto()
    ONEPAIR = auto()
    TWOPAIR = auto()
    THREEOFAKIND = auto()
    FULLHOUSE = auto()
    FOUROFAKIND = auto()
    FIVEOFAKIND = auto()


def cal_strength_type(cards):
    cnter = Counter(cards)
    [(_, most_common_len)] = cnter.most_common(1)
    if len(cnter) == 1:
        strength_type = HandStrength.FIVEOFAKIND
    elif len(cnter) == 2:
        if most_common_len == 4:
            strength_type = HandStrength.FOUROFAKIND
        else:
            strength_type = HandStrength.FULLHOUSE
    elif len(cnter) == 3:
        if most_common_len == 3:
            strength_type = HandStrength.THREEOFAKIND
        else:
            strength_type = HandStrength.TWOPAIR
    elif len(cnter) == 4:
        strength_type = HandStrength.ONEPAIR
    else:
        strength_type = HandStrength.HIGHCARD
    return strength_type


@total_ordering
class Hand:
    def __init__(self, cards, bet):
        self.cards = cards
        self.bet = int(bet)
        self.strength_type = cal_strength_type(cards)

    def __lt__(self, other):
        if isinstance(other, type(self)):
            if self.strength_type != other.strength_type:
                return self.strength_type < other.strength_type
            for c1, c2 in zip(self.cards, other.cards):
                l1, l2 = get_label_enum(c1), get_label_enum(c2)
                if l1 != l2:
                    return l1 < l2
            return False
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.strength_type == other.strength_type and all(
                get_label_enum(c1) == get_label_enum(c2)
                for c1, c2 in zip(self.cards, other.cards)
            )
        return NotImplemented

    def __repr__(self):
        cls_name = type(self).__name__
        return f"{cls_name}(cards={self.cards}, bet={self.bet})"


def parse_input(file_path):
    hands = []
    with open(file_path) as f:
        for line in f:
            cards, bet = line.strip().split()
            hand = Hand(cards, bet)
            hands.append(hand)
    return sorted(hands)


def cal_total_winnings(hands):
    return sum(rank * hand.bet for rank, hand in enumerate(hands, start=1))


if __name__ == "__main__":
    # 251806792
    file_path = Path(__file__).parent.parent / "data/input.txt"
    hands = parse_input(file_path)
    # print(f"{hands=}")
    result = cal_total_winnings(hands)
    print(f"{result=}")
