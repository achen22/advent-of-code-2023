import sys

NUMBERS = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
REPLACE = {NUMBERS[i]: NUMBERS[i][0] + str(i + 1) + NUMBERS[i][1:] for i in range(len(NUMBERS))}

if __name__ == "__main__":
    total = 0
    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for line in f.readlines():
            for k, v in REPLACE.items():
                line = line.replace(k, v)
            left = None
            right = None
            for c in line:
                if c.isdigit():
                    right = int(c)
                    if left is None:
                        left = int(c)
            total += left * 10 + right
    print(total)
