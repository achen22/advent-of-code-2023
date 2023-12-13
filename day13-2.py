import sys

def find_reflection_row(pattern):
    found = {}

    for i in range(len(pattern) - 1):
        original = pattern[i + 1:]
        mirrored = reversed(pattern[:i + 1])
        diff = None
        for a, b in zip(original, mirrored):
            if a != b:
                if diff is not None:
                    diff = None
                    break
                diff = (a, b)
        if diff is not None:
            found[i + 1] = diff

    for k, v in found.items():
        count = 0
        for a, b in zip(*v):
            if a != b:
                if count != 0:
                    count = 0
                    break
                count += 1
        if count == 1:
            return k
    return 0

if __name__ == "__main__":
    patterns = []

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        pattern = []
        for line in f.readlines():
            line = line.rstrip()
            if line:
                pattern.append(line)
            else:
                patterns.append(pattern)
                pattern = []
        patterns.append(pattern)

    total = 0
    for pattern in patterns:
        score = find_reflection_row(pattern)
        if score != 0:
            total += score * 100
        else:
            total += find_reflection_row(list(zip(*pattern)))

    print(total)
