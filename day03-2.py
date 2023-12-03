import sys

if __name__ == "__main__":
    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        schematic = [line.rstrip() for line in f.readlines()]
    row_size = len(schematic[0])
    assert all(len(row) == row_size for row in schematic)

    # (row, col_start, col_stop, value)
    number_positions: list[tuple[int, int, int, int]] = []
    gears: dict[tuple[int, int], list[int]] = {}
    for i, row in enumerate(schematic):
        first_digit = None
        for j, c in enumerate(row):
            if c.isdigit():
                if first_digit is None:
                    first_digit = j
            elif first_digit is not None:
                number_positions.append((i, first_digit, j, int(row[first_digit:j])))
                first_digit = None
            if c == "*":
                gears[(i, j)] = []
        if first_digit is not None:
            number_positions.append((i, first_digit, row_size, int(row[first_digit:row_size])))

    for row, start, stop, value in number_positions:
        adjacent = [(row, start - 1), (row, stop)]
        for i in (row - 1, row + 1):
            for j in range(start - 1, stop + 1):
                adjacent.append((i, j))
        for cell in adjacent:
            if cell in gears:
                gears[cell].append(value)

    total = 0
    for numbers in gears.values():
        if len(numbers) == 2:
            total += numbers[0] * numbers[1]
    print(total)
