import sys

COLOURS = ("red", "green", "blue")

if __name__ == "__main__":
    total = 0

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for line in f.readlines():
            line = line.rstrip().split(": ")[1].split("; ")
            game = {c: 0 for c in COLOURS}
            for hand in line:
                hand = hand.split(", ")
                for cubes in hand:
                    n, colour = cubes.split(" ")
                    n = int(n)
                    game[colour] = max(n, game[colour])
            product = 1
            for n in game.values():
                product *= n
            total += product
    print(total)