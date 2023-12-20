import sys
from collections import deque, Counter

LOW = False
HIGH = True

def frozen(modules):
    result = []
    for name, module in modules.items():
        state = module[1]
        if type(state) is dict:
            state = tuple(k for k, v in state.items() if v == LOW)

        if state is not None:
            result.append((name, state))
    return tuple(result)

def button(modules):
    # (destination, data, source)
    queue = deque()
    queue.append(("broadcaster", LOW, None))

    result = Counter()
    while len(queue) != 0:
        name, pulse, source = queue.popleft()
        result[pulse] += 1
        if name == "output":
            print("high" if pulse else "low")
            continue
        destination, state = modules[name]

        if type(state) is bool:
            # flip-flop module
            if pulse == HIGH:
                continue
            pulse = not state
            modules[name][1] = pulse

        elif type(state) is dict:
            # conjunction module
            state[source] = pulse
            pulse = not all(v for v in state.values())

        else:
            # broadcast module
            assert state is None

        for d in destination:
            queue.append((d, pulse, name))

    return result

def test(modules, r = 1):
    print(frozen(modules))
    count = Counter()
    for _ in range(r):
        count += button(modules)
        print(frozen(modules))
    print(count)

if __name__ == "__main__":
    modules = {}

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for line in f.readlines():
            name, destination = line.rstrip().split(" -> ")
            state = None
            if name[0] == "%":
                name = name[1:]
                state = LOW
            elif name[0] == "&":
                name = name[1:]
                state = {}
            modules[name] = [tuple(destination.split(", ")), state]

    untyped = []
    for name, module in modules.items():
        destination = module[0]
        for d in destination:
            if d not in modules:
                untyped.append(d)
            elif type(modules[d][1]) is dict:
                modules[d][1][name] = LOW
    
    for d in untyped:
        modules[d] = ((), None)

    cache = {}
    prev = frozen(modules)
    while prev not in cache:
        cache[prev] = button(modules)
        prev = frozen(modules)
        #print(".", end="")
        if len(cache) == 1000:
            count = sum(cache.values(), Counter())
            break

    states = list(cache.keys())
    if prev in cache:
        index = states.index(prev) if prev in states else 1000

        #print(start, len(cache))
        count = Counter()
        loops = (1000 - index) // (len(cache) - index)
        for state in states[index:]:
            count += cache[state]
        for k in count.keys():
            count[k] *= loops
        for state in states[:index]:
            count += cache[state]

        step = index + loops * (len(cache) - index)
        while step != 1000:
            count += cache[states[index]]
            index += 1
            step += 1

    print(count[LOW] * count[HIGH])
