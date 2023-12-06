import sys

if __name__ == "__main__":
    total = 0
    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        time = int("".join(f.readline().rstrip().split()[1:]))
        distance = int("".join(f.readline().rstrip().split()[1:]))

    # brute force doesn't take very long...
    #count = 0
    #for i in range(time):
    #    if i * (time - i) > distance:
    #        count += 1
    #print(count)

    # ...but that was too easy, so I'm doing some maths today
    # x * (time - x) == distance
    # x * time - x * x - distance == 0
    # x * x - time * x + distance == 0
    # x = (- (-time) +/- sqrt(time * time - 4 * distance)) / 2
    left = (time - (time * time - 4 * distance) ** 0.5) / 2
    right = (time + (time * time - 4 * distance) ** 0.5) / 2
    
    left = int(left)
    while left * (time - left) <= distance:
        left += 1

    right = int(right) + 1
    while right * (time - right) > distance:
        right += 1

    print(right - left)
