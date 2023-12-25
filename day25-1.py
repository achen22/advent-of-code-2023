import sys
from collections import Counter
from itertools import combinations

if __name__ == "__main__":
    edges = {}

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for line in f.readlines():
            a, line = line.rstrip().split(": ")
            if a not in edges:
                edges[a] = []
            for b in line.split():
                if b not in edges:
                    edges[b] = []
                edges[a].append(b)
                edges[b].append(a)

    used = Counter()

    for start in edges.keys():
        visited = {start}
        frontier = edges[start].copy()
        for v in frontier:
            used[frozenset([start, v])] += 1

        while len(frontier) != 0:
            prev = frontier.copy()
            frontier.clear()
            visited.update(prev)
            for u in prev:
                for v in edges[u]:
                    if v in visited or v in frontier:
                        continue
                    frontier.append(v)
                    used[frozenset([u, v])] += 1

    for combo in combinations(used.most_common(10), r=3):
        combo = tuple(s for s, _ in combo)
        start, end = combo[0]

        visited = {start}
        frontier = edges[start].copy()
        frontier.remove(end)
        visited.update(frontier)

        while len(frontier) != 0:
            u = frontier.pop()
            for v in edges[u]:
                if v in visited:
                    continue
                if frozenset([u, v]) in combo:
                    continue
                if v == end:
                    visited.add(v)
                    frontier.clear()
                    break
                frontier.append(v)
                visited.add(v)

        if end not in visited:
            print(len(visited) * (len(edges) - len(visited)))
            break
