import sys

if __name__ == "__main__":
    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        rocks = [line.rstrip() for line in f.readlines()]

    total = 0
    for line in zip(*rocks):
        weight = len(line)
        for i, c in enumerate(line):
            if c == "O":
                total += weight
                weight -= 1
            elif c == "#":
                weight = len(line) - i - 1

    print(total)
