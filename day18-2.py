import sys
from itertools import pairwise

DIRECTION = {
    "3": (-1, 0),
    "1": (1, 0),
    "2": (0, -1),
    "0": (0, 1)
}

if __name__ == "__main__":
    path = [(0, 0)]
    perimeter = 0

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for line in f.readlines():
            line = line.rstrip().split("#")[-1][:-1]
            d = line[5]
            n = line[:5]
            d = DIRECTION[d]
            n = int(n, 16)
            #print(n, d)
            x, y = path[-1]
            i, j = d
            path.append((x + i * n, y + j * n))
            perimeter += n

    assert path[0] == path[-1]

    # https://en.wikipedia.org/wiki/Shoelace_formula
    area = 0
    for a, b in pairwise(path):
        #print(a, b)
        area += (a[1] + b[1]) * (a[0] - b[0])

    print((perimeter + abs(area)) // 2 + 1)
