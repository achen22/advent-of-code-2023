import sys
from collections import deque

LOW = False
HIGH = True

def frozen(modules):
    result = []
    for name, module in modules.items():
        state = module[1]
        if type(state) is dict:
            state = frozenset(k for k, v in state.items() if v == LOW)

        if state is not None:
            result.append((name, state))
    return tuple(result)

def unfreeze(modules, states):
    for name, state in states:
        if type(state) is frozenset:
            lows = state
            state = modules[name][1]
            for k in state.keys():
                state[k] = k not in lows
        else:
            modules[name][1] = state

def button(modules, subgraphs = None, count = 0):
    # (destination, data, source)
    queue = deque()
    queue.append(("broadcaster", LOW, None))

    result = False
    while len(queue) != 0:
        name, pulse, source = queue.popleft()
        if name == "rx":
            if pulse == LOW:
                result == True
        if subgraphs is not None and name in subgraphs:
            if pulse == LOW:
                subgraphs[name].append(count)

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
            pulse = any(v == LOW for v in state.values())

        else:
            # broadcast/untyped module
            assert state is None

        for d in destination:
            queue.append((d, pulse, name))

    return result

def test(modules):
    expected = frozen(modules)
    unfreeze(modules, expected)
    assert frozen(modules) == expected

    count = 0
    flipflop = []
    for name, module in modules.items():
        state = module[1]
        if type(state) is bool:
            flipflop.append(name)
        elif type(state) is dict:
            print(name, "<-", ",".join(state.keys()))
            count += len(state)
    print(",".join(flipflop))
    count += len(flipflop)
    print(count, 1 << count)

    graph = {k: v[0] for k, v in modules.items()}
    subgraphs = {}
    for name in modules["broadcaster"][0]:
        subgraph = set()
        frontier = [name]
        while len(frontier) != 0:
            a = frontier.pop()
            subgraph.add(a)
            for b in graph[a]:
                if b not in subgraph:
                    frontier.append(b)
        print(name, ":", ",".join(subgraph))
        subgraphs[name] = subgraph
    for name in graph.keys():
        contains = []
        for subgraph, items in subgraphs.items():
            if name in items:
                contains.append(subgraph)
        if len(contains) > 1:
            print(name, "element of {", ", ".join(contains), "} subgraphs")

def brute_force(modules):
    # Probably takes too long to complete
    count = 0
    done = False
    progress = 10
    print(1, end = "")
    while not done:
        count += 1
        done = button(modules)
        if count == progress:
            print(0, end="")
            progress *= 10
    print()
    print(count)

# https://dreampuf.github.io/GraphvizOnline/
def graphviz(modules):
    fname = "day20.txt"
    with open(fname, "w") as f:
        f.write("digraph G {\n")
        
        conjunctions = []
        for name, module in modules.items():
            destination = " ".join(module[0])
            f.write(f"  {name} -> {{{destination}}};\n")
            if type(module[1]) is dict:
                conjunctions.append(name)
        f.write("\n")

        for name in conjunctions:
            f.write(f"  {name} [shape=doublecircle]")
        f.write("\n")

        f.write("  broadcaster [shape=box]\n")
        f.write("  rx [shape=square]\n")
        f.write("}\n")
    print(f"Written to {fname}")

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
    last = None
    for name, module in modules.items():
        destination = module[0]
        for d in destination:
            if d not in modules:
                untyped.append(d)
                if d == "rx":
                    assert last is None
                    last = name
            elif type(modules[d][1]) is dict:
                modules[d][1][name] = LOW

    for d in untyped:
        modules[d] = ((), None)

    #test(modules)
    #graphviz(modules)

    subgraphs = {name: [] for name in modules[last][1].keys()}
    count = 0
    done = False
    while not done:
        count += 1
        button(modules, subgraphs, count)
        if all(len(v) >= 2 for v in subgraphs.values()):
            done = True

    #print(subgraphs)
    product = 1
    for a, b in subgraphs.values():
        assert a * 2 == b
        product *= a
    print(product)
