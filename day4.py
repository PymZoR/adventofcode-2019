from collections import Counter


def is_valid(password):
    password = list(map(int, str(password)))
    double_digit = False

    for i, j in zip(password[:-1], password[1:]):
        if j < i:
            return False

        if i == j:
            double_digit = True

    return double_digit


def is_valid2(password):
    password = list(map(int, str(password)))
    digits_count = Counter(password)

    for i, j in zip(password[:-1], password[1:]):
        if j < i:
            return False

    return (2 in digits_count.values())


input_range = range(124075, 580769)

part1 = len(list(filter(is_valid, input_range)))
assert (part1 == 2150)

part2 = len(list(filter(is_valid2, input_range)))
assert (part2 == 1462)
