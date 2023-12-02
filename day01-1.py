import sys

if __name__ == "__main__":
    total = 0
    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for line in f.readlines():
            left = None
            right = None
            for c in line:
                if c.isdigit():
                    right = int(c)
                    if left is None:
                        left = int(c)
            total += left * 10 + right
    print(total)