import sys

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
        found = False

        for i in range(len(pattern) - 1):
            if pattern[i] == pattern[i + 1]:
                original = pattern[i + 1:]
                mirrored = reversed(pattern[:i + 1])
                if all(a == b for a, b in zip(original, mirrored)):
                    total += (i + 1) * 100
                    found = True
                    break

        if not found:
            pattern = list(zip(*pattern))
            for i in range(len(pattern) - 1):
                if pattern[i] == pattern[i + 1]:
                    original = pattern[i + 1:]
                    mirrored = reversed(pattern[:i + 1])
                    if all(a == b for a, b in zip(original, mirrored)):
                        total += i + 1
                        found = True
                        break
            if not found:
                print("\n".join("".join(col) for col in pattern))

    print(total)
