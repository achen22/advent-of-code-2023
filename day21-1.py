import sys

STEPS = 64

def display(height, width, rocks, destinations):
    for i in range(height):
        for j in range(width):
            if (i, j) in rocks:
                print("#", end="")
            elif (i, j) in destinations:
                print("O", end="")
            else:
                print(".", end="")
        print()

if __name__ == "__main__":
    start = None
    rocks = set()

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    steps = STEPS if len(sys.argv) <= 2 else int(sys.argv[2])
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            for j, c in enumerate(line.rstrip()):
                if c == "#":
                    rocks.add((i, j))
                elif c == "S":
                    assert start is None
                    start = (i, j)
    
    height = i + 1
    width = j + 1

    plots = [{start}, set()]
    even = True
    frontier = {start}

    for _ in range(steps):
        even = not even
        prev = list(frontier)
        frontier.clear()
        for i, j in prev:
            for d in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if d not in rocks:
                    frontier.add(d)
        plots[even].update(frontier)

    #display(height, width, rocks, plots[even])
    print(len(plots[even]))
