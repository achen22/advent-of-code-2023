import sys
from bisect import insort

class Path:
    def __init__(self, steps, world, cost = None, position = None):
        self.steps = steps
        self._world = world

        self.position = None
        self.cost = cost
        if cost is None:
            self.cost = 0
            x = 0
            y = 0
            for i, j in steps:
                x += i
                y += j
                self.cost += world[x][y]
            self.position = (x, y)

        if self.position is None:
            self.position = position
            if position is None:
                self.position = (sum(i for i, _ in steps), sum(j for _, j in steps))

        self.heuristic = self.cost + len(self._world) + len(self._world[0]) - 2 - sum(self.position)

    def next_steps(self):
        if len(self.steps) == 0:
            return [(0, 1), (1, 0)]

        i, j = self.steps[-1]
        result = [(i, j)]
        if i == 0:
            result.extend([(-1, 0), (1, 0)])
        else:
            result.extend([(0, -1), (0, 1)])

        if len(self.steps) >= 3:
            if self.steps[-2] == (i, j) and self.steps[-3] == (i, j):
                result.remove((i, j))

        x, y = self.position
        for i, j in tuple(result):
            if x + i == -1 or x + i == len(self._world):
                result.remove((i, j))
            elif y + j == -1 or y + j == len(self._world[0]):
                result.remove((i, j))

        return result

    def step(self, direction):
        i, j = direction
        x, y = self.position
        position = (x + i, y + j)
        cost = self.cost + self._world[x + i][y + j]
        steps = self.steps + [(i, j)]
        return Path(steps, self._world, cost, position)

if __name__ == "__main__":
    world = []

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for line in f.readlines():
            world.append([int(c) for c in line.rstrip()])

    frontier = []
    frontier.append(Path([(0, 1)], world))
    frontier.append(Path([(1, 0)], world))
    frontier.sort(key=lambda p: -p.heuristic)
    visited = {}
    while True:
        path = frontier.pop()
        if path.position == (len(world) - 1, len(world[0]) - 1):
            print(path.cost)
            break

        if len(path.steps) >= 3:
            d = (path.position, tuple(path.steps[-3:]))
            if d in visited:
                continue
            visited[d] = path.cost

        for d in path.next_steps():
            p = path.step(d)
            if len(p.steps) >= 3:
                d = (p.position, tuple(p.steps[-3:]))
                if d in visited and visited[d] < p.cost:
                    break
            insort(frontier, p, key=lambda p: -p.heuristic)
