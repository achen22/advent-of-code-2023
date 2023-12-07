import sys

CARD = {
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "T": 9,
    "J": 0,
    "Q": 10,
    "K": 11,
    "A": 12
}

if __name__ == "__main__":
    hands = []
    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for line in f.readlines():
            hand, bid = line.rstrip().split(" ")
            assert len(hand) == 5
            hand = tuple(CARD[c] for c in hand)
            bid = int(bid)
            hands.append({"cards": hand, "bid": bid})

    for hand in hands:
        cards = hand["cards"]
        strength = [0] * len(CARD)
        for i in cards:
            strength[i] += 1
        jokers = strength[0]
        strength = sorted(filter(lambda n: n > 0, strength[1:]), reverse=True)
        if len(strength) == 0:
            strength.append(0)
        strength[0] += jokers
        hand["strength"] = strength

    hands.sort(key = lambda hand: (hand["strength"], hand["cards"]))
    total = 0
    for i, hand in enumerate(hands):
        total += (i + 1) * hand["bid"]
    print(total)
