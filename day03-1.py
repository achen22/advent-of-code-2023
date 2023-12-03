import sys

NON_SYMBOLS = frozenset("0123456789.")

if __name__ == "__main__":
    filename = "input" if len(sys.argv) == 1 else sys.argv[1]
    with open(filename) as f:
        schematic = [line.rstrip() for line in f.readlines()]
    row_size = len(schematic[0])
    assert all(len(row) == row_size for row in schematic)

    # (row, col_start, col_stop, value)
    number_positions: list[tuple[int, int, int, int]] = []
    for i, row in enumerate(schematic):
        first_digit = None
        for j, c in enumerate(row):
            if c.isdigit():
                if first_digit is None:
                    first_digit = j
            elif first_digit is not None:
                number_positions.append((i, first_digit, j, int(row[first_digit:j])))
                first_digit = None
        if first_digit is not None:
            number_positions.append((i, first_digit, row_size, int(row[first_digit:row_size])))

    total = 0
    for row, start, stop, value in number_positions:
        if start != 0 and schematic[row][start - 1] != ".":
            total += value
        elif stop != row_size and schematic[row][stop] != ".":
            total += value
        else:
            left = 0 if start == 0 else start - 1
            right = row_size if stop == row_size else stop + 1
            if row != 0 and any(c not in NON_SYMBOLS for c in schematic[row - 1][left:right]):
                total += value
            elif row + 1 != len(schematic) and any(c not in NON_SYMBOLS for c in schematic[row + 1][left:right]):
                total += value
    print(total)
