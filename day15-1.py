import sys

def hsh(s):
    result = 0
    for c in s:
        result += ord(c)
        result *= 17
        result %= 256
    return result

if __name__ == "__main__":
    total = 0

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        s = []
        for c in f.read():
            if c in (",", "\r", "\n"):
                total += hsh(s)
                s.clear()
            else:
                s.append(c)
        if len(s) != 0:
            total += hsh(s)

    print(total)
