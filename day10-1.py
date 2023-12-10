import sys

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)

PIPE = {
    "|": (NORTH, SOUTH),
    "-": (EAST, WEST),
    "L": (NORTH, EAST),
    "J": (NORTH, WEST),
    "7": (SOUTH, WEST),
    "F": (SOUTH, EAST),
    ".": (),
    "S": (NORTH, SOUTH, EAST, WEST)
}

if __name__ == "__main__":
    pipes = []
    start = None

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for line in f.readlines():
            row = [PIPE[c] for c in line.rstrip()]
            if "S" in line:
                start = (len(pipes), line.index("S"))
            pipes.append(row)

    steps = 0
    frontier = {start}
    traversed = set()
    done = False
    while not done:
        prev = list(frontier)
        frontier.clear()
        steps += 1
        for x, y in prev:
            traversed.add((x, y))
            for i, j in pipes[x][y]:
                if x + i in (-1, len(pipes[0])):
                    continue
                if y + j in (-1, len(pipes)):
                    continue
                if len(pipes[x + i][y + j]) != 2:
                    continue
                if (x + i, y + j) in traversed:
                    continue
                if (-i, -j) in pipes[x + i][y + j]:
                    if (x + i, y + j) in frontier:
                        done = True
                    else:
                        frontier.add((x + i, y + j))

    print(steps)
