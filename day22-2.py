import sys
import itertools

def fall(bricks: list[list[tuple[int, int, int]]], check_only: bool = False):
    occupied = set(itertools.chain.from_iterable(bricks))
    result = None

    for brick in bricks:
        if brick[0][2] == 1:
            continue

        occupied.difference_update(brick)
        move = True
        for i, j, k in brick:
            if (i, j, k - 1) in occupied:
                move = False
                break

        while move:
            if check_only:
                return True
            result = tuple(brick)
            brick.clear()
            for i, j, k in result:
                brick.append((i, j, k - 1))
                if k == 2 or (i, j, k - 2) in occupied:
                    move = False

        occupied.update(brick)

    return result is not None

if __name__ == "__main__":
    bricks = []

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for line in f.readlines():
            start, stop = line.rstrip().split("~")
            start = [int(n) for n in start.split(",")]
            stop = tuple(int(n) for n in stop.split(","))

            axis = None
            for i in range(3):
                if start[i] != stop[i]:
                    assert axis is None
                    axis = i

            if axis is None:
                bricks.append([stop])
                continue

            a = start[axis]
            b = stop[axis]
            if a > b:
                a, b = b, a

            brick = []
            for i in range(a, b + 1):
                start[axis] = i
                brick.append(tuple(start))
            bricks.append(brick)

    while fall(bricks):
        pass

    count = 0
    for i in range(len(bricks)):
        before = bricks[:i] + bricks[i + 1:]
        after = [brick.copy() for brick in before]
        while fall(after):
            pass
        for a, b in zip(before, after):
            if a[0][2] != b[0][2]:
                count += 1
    print(count)
