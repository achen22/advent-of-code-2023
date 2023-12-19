import sys

def part_count(part):
    assert all(x in part for x in "xmas")
    result = 1
    for a, b in part.values():
        result *= b - a
    return result

class Workflow:
    def __init__(self, rules):
        rules = rules.split(",")
        self._rules = []
        for rule in rules:
            if ":" not in rule:
                self._rules.append(rule)
                break
            condition, result = rule.split(":")
            f = ">" if ">" in condition else "<"
            x, n = condition.split(f)
            self._rules.append((f, x, int(n), result))

    def evaluate(self, part):
        result = []
        count = part_count(part)
        for f, x, n, y in self._rules[:-1]:
            partial = {k: v for k, v in part.items() if k != x}
            low, high = part[x]
            if f == "<":
                if n < low:
                    result.append((y, partial | {x: (low, high)}))
                    assert sum(part_count(v) for _, v in result) == count
                    return result
                if n < high:
                    assert y not in result
                    result.append((y, partial | {x: (low, n)}))
                    part = partial | {x: (n, high)}
            else:
                n += 1
                if n > high:
                    result.append((y, partial | {x: (low, high)}))
                    assert sum(part_count(v) for _, v in result) == count
                    return result
                if n > low:
                    result.append((y, partial | {x: (n, high)}))
                    part = partial | {x: (low, n)}
        return result + [(self._rules[-1], part)]

if __name__ == "__main__":
    workflows = {}

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        line = f.readline().rstrip()
        while line:
            k, line = line[:-1].split("{")
            workflows[k] = Workflow(line)

            line = f.readline().rstrip()

    part = {x: (1, 4001) for x in "xmas"}
    workflow = [("in", part)]
    total = 0
    while len(workflow) != 0:
        k, v = workflow.pop()
        for k, v in workflows[k].evaluate(v):
            if k == "R":
                continue
            if k == "A":
                total += part_count(v)
            else:
                workflow.append((k, v))
    print(total)
