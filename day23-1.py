import sys

SLOPE = {
    ">": (0, 1),
    "<": (0, -1),
    "v": (1, 0),
    "^": (-1, 0)
}

if __name__ == "__main__":
    spaces = []
    slopes = {}

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            for j, c in enumerate(line.rstrip()):
                if c == ".":
                    spaces.append((i, j))
                elif c in SLOPE:
                    slopes[(i, j)] = SLOPE[c]

    start = spaces[0]
    end = spaces[-1]
    spaces = set(spaces[1:-1])

    count = 0
    frontier = [(start, )]

    while len(frontier) != 0:
        path = frontier.pop()
        if path[-1] in slopes:
            step = tuple(sum(pair) for pair in zip(path[-1], slopes[path[-1]]))
            if step not in path:
                frontier.append(path + (step, ))

        else:
            x, y = path[-1]
            for i, j in SLOPE.values():
                step = (x + i, y + j)
                if step == end:
                    count = max(count, len(path))
                elif (step in spaces or step in slopes) and step not in path:
                    frontier.append(path + (step, ))

    print(count)
