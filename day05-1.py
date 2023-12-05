import sys

if __name__ == "__main__":
    seeds = []
    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        line = f.readline().rstrip()
        assert line.startswith("seeds: ")
        seeds = [int(n) for n in line.split(" ")[1:]]
        assert f.readline().isspace()
        remaining = f.read().split("\n\n")

    mappings: list[dict[tuple[int, int], int]] = []
    for block in remaining:
        block = block.split("\n")[1:]
        mapping: dict[tuple[int, int], int] = {}
        for line in block:
            if not line:
                continue
            a, b, c = (int(n) for n in line.split(" "))
            mapping[(b, b + c)] = a - b
        mappings.append(mapping)

    lowest = None
    for seed in seeds:
        for mapping in mappings:
            #print(seed, end=" ")
            for start, stop in mapping.keys():
                if seed >= start and seed < stop:
                    seed += mapping[(start, stop)]
                    break
        #print(seed)
        if lowest is None or seed < lowest:
            lowest = seed

    print(lowest)
