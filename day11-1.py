import sys
import itertools

if __name__ == "__main__":
    galaxies = []
    offset = 0

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            count = len(galaxies)
            for j, c in enumerate(line.rstrip()):
                if c == "#":
                    galaxies.append([i + offset, j])
            if len(galaxies) == count:
                offset += 1

    columns = {n for _, n in galaxies}
    columns = [n for n in range(max(columns)) if n not in columns]
    for g in galaxies:
        offset = 0
        for c in columns:
            if c < g[1]:
                offset += 1
        g[1] += offset

    total = 0
    for a, b in itertools.combinations(galaxies, 2):
        total += abs(a[0] - b[0]) + abs(a[1] - b[1])
        count += 1

    print(total)
