import sys

DIRECTIONS = ((0, 1), (0, -1), (1, 0), (-1, 0))

if __name__ == "__main__":
    spaces = []
    slopes = {}

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            for j, c in enumerate(line.rstrip()):
                if c in ".<>^v":
                    spaces.append((i, j))

    start = spaces[0]
    end = spaces[-1]
    spaces = set(spaces)

    vertices = {}
    edges = {}
    for x, y in spaces:
        directions = tuple((x + i, y + j) for i, j in DIRECTIONS if (x + i, y + j) in spaces)
        if len(directions) != 2:
            assert len(directions) != 0
            vertices[(x, y)] = [[(x, y), d] for d in directions]
        else:
            edges[(x, y)] = directions
    assert end in vertices

    for k in vertices.keys():
        for path in vertices[k]:
            while path[-1] not in vertices:
                a, b = edges[path[-1]]
                path.append(a if b == path[-2] else b)
        vertices[k] = {path[-1]: len(path) - 1 for path in vertices[k]}
    #print(vertices)

    count = 0
    frontier = [((start, ), 0)]

    while len(frontier) != 0:
        path, cost = frontier.pop()
        prev = path[-1]
        for step in vertices[prev].keys():
            new_cost = cost + vertices[prev][step]
            if step == end:
                total = new_cost
                if total > count:
                    count = total
                    #print(total)
            elif step not in path:
                frontier.append((path + (step, ), new_cost))

    print(count)
