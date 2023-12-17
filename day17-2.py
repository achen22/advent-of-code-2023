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
        
        self.stopped = len(self.steps) >= 4 and all(s == self.steps[-1] for s in self.steps[-4:-1])
        self.heuristic = self.cost + len(self._world) + len(self._world[0]) - 2 - sum(self.position)
        
        count = 0
        self.state = (self.position, (0, 0), 0)
        if len(self.steps) != 0:
            count = 1
            step = self.steps[-1]
            while len(self.steps) != count and self.steps[-count-1] == step:
                count += 1
            self.state = (self.position, step, count)

    def next_steps(self):
        if len(self.steps) == 0:
            return [(0, 1), (1, 0)]

        i, j = self.steps[-1]
        result = [(i, j)]
        if self.stopped:
            if i == 0:
                result.extend([(-1, 0), (1, 0)])
            else:
                result.extend([(0, -1), (0, 1)])

        if len(self.steps) >= 10:
            if all(s == (i, j) for s in self.steps[-10:-4]):
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

        if path.stopped:
            if path.position == (len(world) - 1, len(world[0]) - 1):
                print(path.cost)
                break

        if path.state in visited:
            continue
        visited[path.state] = path.cost

        for d in path.next_steps():
            p = path.step(d)
            if p.state in visited and visited[p.state] < p.cost:
                break
            insort(frontier, p, key=lambda p: -p.heuristic)
