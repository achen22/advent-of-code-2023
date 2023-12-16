import sys

if __name__ == "__main__":
    mirrors = {}
    splitters = {}

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            for j, c in enumerate(line.rstrip()):
                if c == "|":
                    splitters[(i, j)] = 0
                elif c == "-":
                    splitters[(i, j)] = 1
                elif c == "\\":
                    mirrors[(i, j)] = 1
                elif c == "/":
                    mirrors[(i, j)] = -1

    height = i + 1
    width = j + 1

    alignments = []
    for i in range(height):
        alignments.append(((i, 0), (0, 1)))
        alignments.append(((i, width - 1), (0, -1)))
    for j in range(width):
        alignments.append(((0, j), (1, 0)))
        alignments.append(((height - 1, j), (-1, 0)))

    total = 0
    for alignment in alignments:
        wavefront = [alignment]
        energised = set()
        while len(wavefront) != 0:
            cell, direction = wavefront.pop()
            if (cell, direction) in energised:
                continue

            i, j = cell
            if i == -1 or i == height or j == -1 or j == width:
                continue

            energised.add((cell, direction))

            if cell in splitters:
                if direction[splitters[cell]] == 0:
                    direction = tuple(reversed(direction))
                    wavefront.append((tuple(sum(pair) for pair in zip(cell, direction)), direction))
                    direction = tuple(-k for k in direction)
            elif cell in mirrors:
                direction = tuple(reversed([mirrors[cell] * k for k in direction]))
            wavefront.append((tuple(sum(pair) for pair in zip(cell, direction)), direction))

        total = max(total, len({cell for cell, _ in energised}))
    print(total)
