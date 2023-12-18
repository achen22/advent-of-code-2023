import sys

DIRECTION = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1)
}

def display(dig):
    for x in range(min(i for i, _ in dig), max(i for i, _ in dig) + 1):
        for y in range(min(j for _, j in dig), max(j for _, j in dig) + 1):
            print("#" if (x, y) in dig else ".", end="")
        print()

if __name__ == "__main__":
    dig = {(0, 0)}
    position = [0, 0]

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for line in f.readlines():
            d, n, _ = line.rstrip().split(" ")
            d = DIRECTION[d]
            n = int(n)
            for _ in range(n):
                for i in range(2):
                    position[i] += d[i]
                dig.add(tuple(position))

    #display(dig)
    frontier = {(1, 1)}
    fill = set()
    while len(frontier) != 0:
        x, y = frontier.pop()
        fill.add((x, y))
        for i, j in DIRECTION.values():
            i += x
            j += y
            if (i, j) not in dig and (i, j) not in fill:
                frontier.add((i, j))

    #display(dig | fill)
    print(len(dig) + len(fill))
