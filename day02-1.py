import sys

LIMIT = {
    "red": 12,
    "green": 13,
    "blue": 14
}

if __name__ == "__main__":
    games = []

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for line in f.readlines():
            line = line.rstrip().split(": ")[1].split("; ")
            game = {c: 0 for c in LIMIT.keys()}
            for hand in line:
                hand = hand.split(", ")
                for cubes in hand:
                    n, colour = cubes.split(" ")
                    n = int(n)
                    game[colour] = max(n, game[colour])
            games.append(game)
    
    #print(games)
    total = 0
    for i, game in enumerate(games):
        if not any(game[c] > LIMIT[c] for c in LIMIT.keys()):
            total += i + 1
    print(total)