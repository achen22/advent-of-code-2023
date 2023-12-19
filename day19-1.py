import sys

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
        for f, x, n, result in self._rules[:-1]:
            if f == "<":
                if part[x] < n:
                    return result
            elif part[x] > n:
                return result
        return self._rules[-1]

if __name__ == "__main__":
    workflows = {}
    parts = []

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        line = f.readline().rstrip()
        while line:
            k, line = line[:-1].split("{")
            workflows[k] = Workflow(line)

            line = f.readline().rstrip()

        for line in f.readlines():
            line = line.rstrip()[1:-1].split(",")
            line = [s.split("=") for s in line]
            parts.append({k: int(v) for k, v in line})

    total = 0
    for part in parts:
        workflow = "in"
        while workflow != "R":
            workflow = workflows[workflow].evaluate(part)
            if workflow == "A":
                total += sum(part.values())
                break

    print(total)
