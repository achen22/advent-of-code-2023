import sys
import itertools

if __name__ == "__main__":
    history = []

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for line in f.readlines():
            history.append([int(n) for n in line.rstrip().split(" ")])

    total = 0
    for values in history:
        start = values[0]
        diffs = [values]
        diff = [b - a for a, b in itertools.pairwise(values)]
        while len(diff) > 1 and any(d != diff[0] for d in diff[1:]):
            diffs.append(diff)
            diff = [b - a for a, b in itertools.pairwise(diff)]
        total += diff[0] + sum(d[-1] for d in diffs)

    print(total)
