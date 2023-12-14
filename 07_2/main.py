from typing import List, Optional
from functools import cmp_to_key


CARDS = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


def read_lines() -> List[str]:
    with open("data.txt", "r") as f:
        lines = f.readlines()
        lines = [l[:-1] if "\n" in l else l for l in lines]
    return lines


def joker_count(hand: str) -> int:
    return sum([1 for c in hand if c == "J"])


def card_count(hand: str, card: str) -> int:
    return sum([1 for c in hand if c == card])


def is_set_of(hand: str, count: int) -> Optional[str]:
    return next(iter(([c for c in CARDS[1:] if card_count(hand, c) + joker_count(hand) == count])), None)


def is_full_house(hand: str) -> bool:
    jokers = joker_count(hand)
    if jokers >= 3:
        return True
    elif jokers == 2:
        return any([c for c in CARDS[1:] if card_count(hand, c) == 2])
    elif jokers == 1:
        return len([c for c in CARDS[1:] if card_count(hand, c) == 2]) == 2
    else: # jokers == 0
        c3 = next(iter([c for c in CARDS if card_count(hand, c) == 3]))
        h = hand.replace(c3, "")
        return h[0] == h[1]


def is_two_pair(hand: str) -> bool:
    jokers = joker_count(hand)
    if jokers >= 2:
        return True
    elif jokers == 1:
        return any([c for c in CARDS[1:] if card_count(hand, c) == 2])
    else: # jokers == 0
        return len([c for c in CARDS[1:] if card_count(hand, c) == 2]) == 2


def hand_score(hand: str) -> int:
    if is_set_of(hand, 5):
        return 6
    elif is_set_of(hand, 4):
        return 5
    elif is_set_of(hand, 3):
        if is_full_house(hand):
            return 4
        else:
            return 3
    elif is_set_of(hand, 2):
        if is_two_pair(hand):
            return 2
        else:
            return 1
    return 0


def compare_lex(h1: str, h2: str) -> int:
    for c1, c2 in zip(h1, h2):
        diff = CARDS.index(c1) - CARDS.index(c2)
        if diff != 0:
            return diff
    return 0


def compare(h1: str, h2: str) -> int:
    diff = hand_score(h1) - hand_score(h2)
    if diff != 0:
        return diff
    else:
        return compare_lex(h1, h2)


def main():
    lines = read_lines()
    hands_with_bids = [(l.split(" ")[0].strip(), int(l.split(" ")[1]))
                       for l in lines if l != ""]
    hands_with_bids = sorted(hands_with_bids, key=cmp_to_key(lambda x, y: compare(x[0], y[0])))
    winnings = [bid * rank for (hand, bid), rank
                in zip(hands_with_bids, range(1, len(hands_with_bids)+1))]
    print("total winnings are", sum(winnings))


if __name__ == "__main__":
    main()
