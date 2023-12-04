import sys

if __name__ == "__main__":
    cards = []
    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for line in f.readlines():
            winners, numbers = line.rstrip().split(":")[1].strip().split(" | ")
            winners = [int(n) for n in winners.split(" ") if n]
            numbers = [int(n) for n in numbers.split(" ") if n]
            cards.append((winners, numbers))

    total = 0
    for winners, numbers in cards:
        matches = 0
        for n in winners:
            if n in numbers:
                matches += 1
        if matches != 0:
            total += 1 << (matches - 1)
    print(total)
