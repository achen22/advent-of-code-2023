import sys

def display(circles, squares, height, width):
    for i in range(height):
        for j in range(width):
            if (i, j) in circles:
                print("O", end="")
            elif (i, j) in squares:
                print("#", end="")
            else:
                print(".", end="")
        print()

def weight(circles, height):
    return height * len(circles) - sum(c[0] for c in circles)

def rotate_clockwise(rocks, width):
    result = set()
    for i, j in rocks:
        result.add((j, width - i - 1))
    return result

def rotate_anticlockwise(rocks, height):
    result = set()
    for i, j in rocks:
        result.add((height - j - 1, i))
    return result

def tilt_west(circles, squares, height, width):
    result = set()
    for i in range(height):
        j_new = 0
        for j in range(width):
            if (i, j) in circles:
                result.add((i, j_new))
                j_new += 1
            elif (i, j) in squares:
                j_new = j + 1
    return result

def cycle(circles, squares, height, width):
    circles = rotate_anticlockwise(circles, height)
    squares = rotate_anticlockwise(squares, height)
    height, width = width, height
    circles = tilt_west(circles, squares, width, height)

    circles = rotate_clockwise(circles, width)
    squares = rotate_clockwise(squares, width)
    height, width = width, height
    circles = tilt_west(circles, squares, width, height)

    circles = rotate_clockwise(circles, width)
    squares = rotate_clockwise(squares, width)
    height, width = width, height
    circles = tilt_west(circles, squares, width, height)

    circles = rotate_clockwise(circles, width)
    squares = rotate_clockwise(squares, width)
    height, width = width, height
    circles = tilt_west(circles, squares, width, height)

    return set((height - i - 1, width - j - 1) for i, j in circles)

def test(circles, squares, height, width):
    display(circles, squares, height, width)
    #print(weight(circles, height))

    #circles = rotate(circles, height)
    #squares = rotate(squares, height)
    #display(circles, squares, width, height)

    print()
    #circles = tilt(circles, squares, width, height)
    #display(circles, squares, width, height)
    circles = cycle(circles, squares, width, height)
    print("After 1 cycle:")
    display(circles, squares, width, height)

    print()
    circles = cycle(circles, squares, width, height)
    print("After 2 cycles:")
    display(circles, squares, width, height)

    print()
    circles = cycle(circles, squares, width, height)
    print("After 3 cycles:")
    display(circles, squares, width, height)

if __name__ == "__main__":
    squares = set()
    circles = set()

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            for j, c in enumerate(line.rstrip()):
                if c == "O":
                    circles.add((i, j))
                elif c == "#":
                    squares.add((i, j))
        
    height = i + 1
    width = j + 1

    #test(circles, squares, height, width)

    cache = [circles]
    for _ in range(1000000000):
        circles = cycle(circles, squares, width, height)
        if circles in cache:
            break
        cache.append(circles)

    index = (1000000000 - cache.index(circles)) % (len(cache) - cache.index(circles)) + cache.index(circles)
    print(weight(cache[index], height))
