import sys

def row_to_list(row):
    return [str_to_list(s) for s in row.split(".") if s]

def str_to_list(s):
    result = []
    q = True
    count = 0
    for c in s:
        if q != (c == "?"):
            result.append(count)
            q = not q
            count = 0
        count += 1
    result.append(count)
    return result

solutions_cache = {}

def count_solutions(pattern, current):
    if len(pattern) == 0:
        return all(len(l) == 1 for l in current)

    if len(current) == 0:
        return 0

    if type(pattern) is not tuple:
        pattern = tuple(pattern)

    current_tuple = tuple(tuple(l) for l in current)
    current_tuple = (pattern, current_tuple)
    if current_tuple in solutions_cache:
        return solutions_cache[current_tuple]

    result = 0
    current = current[:]
    block = current[0][:]

    # first character is ?
    if block[0] != 0:
        block[0] -= 1
        if len(block) == 1 and block[0] == 0:
            result += count_solutions(pattern, current[1:])
        else:
            result += count_solutions(pattern, [block] + current[1:])

        if block[0] == 0:
            if len(block) == 1:
                current[0] = [0, 1]
            else:
                block[1] += 1
                current[0] = block
        else:
            current[0] = [0, 1] + block
        result += count_solutions(pattern, current)
        solutions_cache[current_tuple] = result
        return result

    # too many in block
    if block[1] > pattern[0]:
        solutions_cache[current_tuple] = 0
        return 0

    # starts with correct pattern
    if block[1] == pattern[0]:
        if len(block) == 2:
            result = count_solutions(pattern[1:], current[1:])
            solutions_cache[current_tuple] = result
            return result
        block = block[2:]
        block[0] -= 1
        if len(block) == 1:
            if block[0] <= 0:
                result = count_solutions(pattern[1:], current[1:])
                solutions_cache[current_tuple] = result
                return result
        result = count_solutions(pattern[1:], [block] + current[1:])
        solutions_cache[current_tuple] = result
        return result

    # not enough in block
    if len(block) == 2:
        return 0
    block[1] += 1
    block[2] -= 1
    if block[2] == 0:
        if len(block) == 3:
            result = count_solutions(pattern, [block[:2]] + current[1:])
            solutions_cache[current_tuple] = result
            return result
        block = [0, block[1] + block[3]] + block[4:]
    result = count_solutions(pattern, [block] + current[1:])
    solutions_cache[current_tuple] = result
    return result

if __name__ == "__main__":
    springs = []

    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        for line in f.readlines():
            row, pattern = line.rstrip().split(" ")
            pattern = [int(n) for n in pattern.split(",")]

            springs.append((row, pattern))

    count = 0
    for row, pattern in springs:
        #print(row, ",".join(str(n) for n in pattern))
        #print(row_to_list(row))
        count += count_solutions(pattern * 5, row_to_list("?".join([row] * 5)))

    print(count)
