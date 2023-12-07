import sys

CARD = {
    "2": 0,
    "3": 1,
    "4": 2,
    "5": 3,
    "6": 4,
    "7": 5,
    "8": 6,
    "9": 7,
    "T": 8,
    "J": 9,
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
        strength = sorted(filter(lambda n: n > 1, strength), reverse=True)
        hand["strength"] = strength
    
    hands.sort(key = lambda hand: (hand["strength"], hand["cards"]))
    total = 0
    for i, hand in enumerate(hands):
        total += (i + 1) * hand["bid"]
    print(total)
