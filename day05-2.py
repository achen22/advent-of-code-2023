import sys
import itertools

if __name__ == "__main__":
    seeds = []
    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        line = f.readline().rstrip()
        assert line.startswith("seeds: ")
        seeds = [int(n) for n in line.split(" ")[1:]]
        assert f.readline().isspace()
        remaining = f.read().split("\n\n")

    seeds = [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]
    seeds.sort()
    #print(seeds)
    for a, b in itertools.pairwise(seeds):
        assert(a[1] < b[0])
    seeds = list(itertools.chain.from_iterable(seeds))
    
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

    mapped = []
    for mapping in mappings:
        diffs = [(k[0], v) for k, v in mapping.items()]
        diff_ends = [(k[1], 0) for k in mapping.keys()]
        for k, _ in diffs:
            if (k, 0) in diff_ends:
                diff_ends.remove((k, 0))
        diffs.extend(diff_ends)
        diffs.sort()

        i = 0
        j = 0
        seeding = None
        diff = 0
        while i < len(seeds) and j < len(diffs):
            a = seeds[i]
            b, c = diffs[j]
            if a < b:
                if seeding is None:
                    seeding = seeds[i]
                else:
                    if seeding != a:
                        mapped.append((seeding + diff, a + diff))
                    seeding = None
                i += 1
            else:
                if seeding is not None and b != seeding:
                    mapped.append((seeding + diff, b + diff))
                    seeding = b
                diff = c
                j += 1
        assert i == len(seeds) or diff == 0
        while i < len(seeds):
            if seeding is None:
                seeding = seeds[i]
            else:
                mapped.append((seeding, seeds[i]))
                seeding = None
            i += 1
        #print(mapped)
        seeds.clear()
        mapped.sort()
        left = mapped[0][0]
        for a, b in itertools.pairwise(mapped):
            if a[1] < b[0]:
                seeds.append(left)
                seeds.append(a[1])
                left = b[0]
        seeds.append(left)
        seeds.append(b[1])
        #print(seeds)
        mapped.clear()
    print(seeds[0])
