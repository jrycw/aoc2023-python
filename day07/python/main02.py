from collections import Counter
from enum import IntEnum, auto
from functools import total_ordering
from pathlib import Path


class CardLabelStrength(IntEnum):
    J = auto()  # should be here?
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    T = auto()
    Q = auto()
    K = auto()
    A = auto()


label_mapping = CardLabelStrength.__members__
label_str_mapping = dict(
    zip(
        list("J23456789TQKA"),
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
    def __init__(self, cards, bet=0, special_label="J"):
        self._orig_cards = cards
        self.cards = cards
        self._special_label = special_label
        if self._special_label in cards:
            self._mutate_cards_if_joker()
        self.bet = int(bet)
        self.strength_type = cal_strength_type(self.cards)

    def _mutate_cards_if_joker(self):
        combo = []
        replacement = list("23456789TJQKA")
        replacement.remove(self._special_label)
        len_repl = len(replacement)
        for card in self.cards:
            if card != self._special_label:
                combo.append(card * len_repl)
            else:
                combo.append(list(replacement))
        best_hand = max([Hand("".join(c)) for c in zip(*combo)])
        self.cards = best_hand.cards

    def __lt__(self, other):
        if isinstance(other, type(self)):
            if self.strength_type != other.strength_type:
                return self.strength_type < other.strength_type
            for c1, c2 in zip(self._orig_cards, other._orig_cards):
                l1, l2 = get_label_enum(c1), get_label_enum(c2)
                if l1 != l2:
                    return l1 < l2
            return False
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.strength_type == other.strength_type and all(
                get_label_enum(c1) == get_label_enum(c2)
                for c1, c2 in zip(self._orig_cards, other._orig_cards)
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
            hands.append(Hand(cards, bet))
    return sorted(hands)


def cal_total_winnings(hands):
    return sum(rank * hand.bet for rank, hand in enumerate(hands, start=1))


if __name__ == "__main__":
    # 252113488
    file_path = Path(__file__).parent.parent / "data/input.txt"
    hands = parse_input(file_path)
    # print(f"sorted: {hands=}")
    result = cal_total_winnings(hands)
    print(f"{result=}")
