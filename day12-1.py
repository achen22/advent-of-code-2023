import sys
from itertools import combinations_with_replacement
from collections import Counter

if __name__ == "__main__":
    springs = []

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for line in f.readlines():
            broken = []
            unknown = []
            row, pattern = line.rstrip().split(" ")
            pattern = [int(n) for n in pattern.split(",")]

            i = 0
            dot = False
            for c in row:
                if c == "#":
                    broken.append(i)
                    dot = False
                    i += 1
                elif c == "?":
                    unknown.append(i)
                    dot = False
                    i += 1
                elif not dot:
                    dot = True
                    i += 1

            springs.append((broken, unknown, pattern, i + dot))

    count = 0
    for initial, unknown, pattern, length in springs:
        index = 0
        ranges = []
        for n in pattern:
            ranges.append((index, index + n))
            index += n + 1

        extra = length - (sum(pattern) + len(pattern) - 1)
        initial = set(initial)
        unknown = set(unknown).union(initial)
        for combination in combinations_with_replacement(range(len(ranges) + 1), extra):
            counter = Counter(combination)
            offset = 0
            pattern = set()
            for i in range(len(ranges)):
                offset += counter[i]
                start, stop = ranges[i]
                pattern.update(range(start + offset, stop + offset))
            if initial.issubset(pattern) and pattern.issubset(unknown):
                count += 1
                #for i in range(max(pattern) + 1):
                #    print("#" if i in pattern else ".", end="")
                #print()

    print(count)
