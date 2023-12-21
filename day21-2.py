import sys
from itertools import pairwise

STEPS = 26501365

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
    print()

def slices(radius):
    a = radius ** 2
    b = a
    if radius & 1 == 1:
        a -= 2 * radius - 1
    else:
        b -= 2 * radius - 1
    return (a, b)

# answer is too high
def first_attempt(start, rocks, height, width):
    for i in (0, start[0], height - 1):
        assert all((i, j) not in rocks for j in range(width))
    for j in (0, start[1], width - 1):
        assert all((i, j) not in rocks for i in range(height))

    assert start[0] == start[1]
    assert STEPS % height == start[0]

    plots = [set(), {start}]
    even = True
    frontier = {start}
    steps = 0

    while len(frontier) != 0:
        prev = list(frontier)
        even = not even
        steps += 1
        frontier.clear()
        for i, j in prev:
            for d in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                exclude = d in rocks
                exclude |= d in plots[even]
                exclude |= d[0] in (-1, height)
                exclude |= d[1] in (-1, width)
                if not exclude:
                    frontier.add(d)
        plots[even].update(frontier)

    assert steps == height
    #print(plots[even])

    assert STEPS % height == start[0]
    radius = STEPS // height
    sizes = tuple(len(plot) for plot in plots)
    plot_count = slices(radius)
    if STEPS & 1 == 1:
        sizes = tuple(reversed(sizes))
    total = sum(a * b for a, b in zip(sizes, plot_count))
    #print(total)

    rocks2 = rocks.copy()
    for k in range(1, 3):
        for i in range(k + 1):
            j = k - i
            for x, y in ((i, j), (i, -j), (-i, j), (-i, -j)):
                rocks2.update((a + x * height, b + y * width) for a, b in rocks)
    
    plots = [set(), {start}]
    even = True
    frontier = {start}
    
    for _ in range(2 * height + start[0]):
        prev = list(frontier)
        even = not even
        frontier.clear()
        for i, j in prev:
            for d in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                exclude = d in rocks2
                exclude |= d in plots[even]
                if not exclude:
                    frontier.add(d)
        plots[even].update(frontier)

    borders = {d: set() for d in ("n", "s", "e", "w", "ne", "se", "sw", "nw")}
    for i, j in plots[even]:
        d = None
        if i < -height:
            d = "n"
            borders[d].add((i + height, j))
        elif i >= 2 * height:
            d = "s"
            borders[d].add((i - height, j))

        if j < -width:
            d = "w"
            borders[d].add((i, j + width))
        elif j >= 2 * width:
            d = "e"
            borders[d].add((i, j - width))

        if d is not None:
            continue

        if i < 0 and j < 0:
            d = "nw"
        elif i >= height and j < 0:
            d = "sw"
        elif i >= height and j >= width:
            d = "se"
        elif i < 0 and j >= width:
            d = "ne"
        if d is not None:
            borders[d].add((i, j))

    total += sum(len(borders[d]) for d in "nsew")
    for d in ("ne", "se", "sw", "nw"):
        total += (radius - 1) * len(borders[d])
        total += (radius - 2) * len(borders[d[0]] & borders[d[1]])
        #display(height, width, rocks, {(i % height, j % width) for i, j in borders[d]})
        #display(height, width, rocks, {(i % height, j % width) for i, j in borders[d[0]] & borders[d[1]]})
    print(total)
    #print(len(plots[even]))

if __name__ == "__main__":
    start = None
    rocks = set()

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    step_target = STEPS if len(sys.argv) <= 2 else int(sys.argv[2])
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
    assert height == width

    plots = [set(), {start}]
    even = True
    frontier = {start}
    steps = step_target % (height * 2)
    rocks2 = rocks.copy()
    for k in range(1, 3):
        for i in range(k + 1):
            j = k - i
            for x, y in ((i, j), (i, -j), (-i, j), (-i, -j)):
                rocks2.update((a + x * height, b + y * width) for a, b in rocks)

    for _ in range(steps):
        prev = list(frontier)
        even = not even
        frontier.clear()
        for i, j in prev:
            for d in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                exclude = d in rocks2
                exclude |= d in plots[even]
                if not exclude:
                    frontier.add(d)
        plots[even].update(frontier)

    #display(height, width, rocks, plots[even])
    #print(steps, ":", len(plots[even]))
    total = len(plots[even])
    counts = [total]

    loop = 0
    diff = 0 if steps == step_target else None
    initial = 0
    while diff is None:
        for k in range(2 * loop + 3, 2 * loop + 5):
            for i in range(k + 1):
                j = k - i
                for x, y in ((i, j), (i, -j), (-i, j), (-i, -j)):
                    rocks2.update((a + x * height, b + y * width) for a, b in rocks)
        loop += 1

        for _ in range(2 * height):
            prev = list(frontier)
            even = not even
            frontier.clear()
            for i, j in prev:
                for d in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                    exclude = d in rocks2
                    exclude |= d in plots[even]
                    if not exclude:
                        frontier.add(d)
            plots[even].update(frontier)

            steps += 1
            if steps == STEPS:
                diff = 0
                total = len(plots[even])
                break
        #print(steps, ":", len(plots[even]))

        # https://en.wikipedia.org/wiki/Arithmetic_progression
        if diff != 0:
            counts.append(len(plots[even]))
            if len(counts) < 4:
                continue
            if len(counts) == 5:
                counts = counts[1:]
            diff = [b - a for a, b in pairwise(counts)]
            diff = [b - a for a, b in pairwise(diff)]
            if all(d == diff[0] for d in diff):
                diff = diff[0]
                initial = counts[-1] - counts[-2]
                total = counts[-2]
            else:
                diff = None

    count = (step_target - steps) // height
    assert count % 1 == 0
    count //= 2
    total += (count + 1) * (initial * 2 + (count) * diff) // 2
    print(total)
