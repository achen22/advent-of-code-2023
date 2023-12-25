import sys
from itertools import combinations

BOUNDS = (200000000000000, 400000000000000)

if __name__ == "__main__":
    stones = []

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for line in f.readlines():
            stone = line.rstrip().split(" @ ")
            stone = [tuple(int(n) for n in v.split(", ")) for v in stone]
            stones.append(tuple(stone))

    count = 0
    for stone1, stone2 in combinations(stones, r=2):
        x1, v1 = stone1
        x2, v2 = stone2
        if v2[1] * v1[0] == v2[0] * v1[1]:
            print("parallel:", v1[:2], v2[:2])
            continue

        m1 = v1[1] / v1[0]
        m2 = v2[1] / v2[0]
        c1 = x1[1] - x1[0] * m1
        c2 = x2[1] - x2[0] * m2
        x_int = (c1 - c2) / (m2 - m1)
        if x_int < BOUNDS[0] or x_int > BOUNDS[1]:
            #print("x_int out of bounds:", x_int)
            continue

        done = False
        for x, v in (stone1, stone2):
            if (x_int - x[0]) / v[0] < 0:
                #print("crossed in the past for", (x, v))
                done = True
                break
        if done:
            continue

        y_int = (c1 * m2 - c2 * m1) / (m2 - m1)
        if y_int < BOUNDS[0] or y_int > BOUNDS[1]:
            #print("y_int out of bounds:", y_int)
            continue

        #print(x_int, y_int)
        count += 1

    print(count)
