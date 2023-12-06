import sys

if __name__ == "__main__":
    total = 0
    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        times = [int(n) for n in f.readline().rstrip().split()[1:]]
        distances = [int(n)  for n in f.readline().rstrip().split()[1:]]
    
    total = 1
    for time, distance in zip(times, distances):
        count = 0
        for i in range(time):
            if i * (time - i) > distance:
                count += 1
        total *= count
    
    print(total)
