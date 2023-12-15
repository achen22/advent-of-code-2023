import sys

def hsh(s):
    result = 0
    for c in s:
        result += ord(c)
        result *= 17
        result %= 256
    return result

def update_hashmap(hmap, l):
    s = "".join(l)
    if s[-1] == "-":
        s = s[:-1]
        label = hsh(s)
        if s in hmap[label]:
            del hmap[label][s]
    else:
        s, v = s.split("=")
        label = hsh(s)
        hmap[label][s] = int(v)

if __name__ == "__main__":
    # Note: dict is ordered since Python 3.7
    hmap = [{} for _ in range(256)]

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        l = []
        for c in f.read():
            if c in (",", "\r", "\n"):
                update_hashmap(hmap, l)
                l.clear()
            else:
                l.append(c)
        if len(l) != 0:
            update_hashmap(hmap, l)

    total = 0
    for i, box in enumerate(hmap):
        for j, k in enumerate(box.values()):
            total += (i + 1) * (j + 1) * k
    print(total)
