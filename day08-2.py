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

    locations = list(filter(lambda l: l[2] == "A", network.keys()))
    counts = []
    for location in locations:
        step = location
        steps = [step]
        z = None

        for d in itertools.cycle(instructions):
            step = network[step][d]
            if step[2] == "Z":
                assert z is None
                z = len(steps)
            if step in steps:
                count = len(steps) - steps.index(step)
                if count % len(instructions) == 0:
                    #print(count, len(steps), count / len(instructions))
                    # note: count // len(instructions) seems to always be a prime number
                    assert steps[-count] == step
                    break
            steps.append(step)

        assert z == count
        counts.append(z // len(instructions))

    #print(counts)
    total = 1
    for n in counts:
        total *= n
    print(total * len(instructions))
