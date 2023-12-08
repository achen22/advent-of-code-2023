import sys
import itertools

if __name__ == "__main__":
    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        instructions = f.readline().rstrip()
        assert len(f.readline().rstrip()) == 0

        network = {}
        for line in f.readlines():
            prev, current = line.rstrip().split(" = ")
            assert current[0] == "(" and current[9] == ")"
            network[prev] = {"L": current[1:4], "R": current[6:9]}

    steps = 0
    location = "AAA"
    for d in itertools.cycle(instructions):
        location = network[location][d]
        steps += 1
        if location == "ZZZ":
            break

    print(steps)
