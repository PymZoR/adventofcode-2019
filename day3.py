from itertools import product

DX = dict(zip('LRUD', [-1, 1, 0, 0]))
DY = dict(zip('LRUD', [0, 0, 1, -1]))


def do_overlap(a, b):
    return (a[1], b[1]) >= max(a[0], b[0])


def compute_intersection(segment1, segment2):
    # Aliases
    x1, y1 = segment1[0]
    x2, y2 = segment1[1]
    x3, y3 = segment2[0]
    x4, y4 = segment2[1]

    # Supperposed lines
    if (x1 == x2 == x3 == x4) or (y1 == y2 == y3 == y4):
        return None

    # Parallel lines
    if (x1 == x2 and x3 == x4) or (y1 == y2 and y3 == y4):
        return None

    # No mutual x
    if not do_overlap([x1, x2], [x3, x4]):
        return None

    # No mutual y
    if not do_overlap([y1, y2], [y3, y4]):
        return None

    xi = x1 if x1 == x2 else x3
    yi = y1 if y1 == y2 else y3

    return (xi, yi)


def compute_polyline_from_wire(wire):
    lines = []
    currentX, currentY = 0, 0

    for movement in wire:
        line = [(currentX, currentY)]
        type, val = movement[:1], int(movement[1:])
        assert type in 'LRUD'

        currentX += DX[type] * val
        currentY += DY[type] * val

        line.append((currentX, currentY))
        lines.append(line)

    return lines


def manhattan(point):
    return abs(point[0]) + abs(point[1])


def wire_dist(polyline, point):
    x, y = point

    total_dist = 0
    for line in polyline:
        x1, y1 = line[0]
        x2, y2 = line[1]

        # Point in line
        if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
            total_dist = total_dist + manhattan([x-x1, y-y1])
            break
        else:
            total_dist = total_dist + manhattan([x1-x2, y1-y2])

    return total_dist


with open('day3.data', 'r') as data:
    data = [line.split(',') for line in data.read().split()]

    polylines = map(compute_polyline_from_wire, data)
    line_couples = product(*polylines)

    intersections = map(lambda x: compute_intersection(*x), line_couples)
    intersections = filter(lambda x: x, intersections)

    part1 = map(manhattan, intersections)
    assert min(part1) == 23

    def wires_dist(x):
        return wire_dist(polylines[0], x) + wire_dist(polylines[1], x)

    part2 = map(wires_dist, intersections)
    assert min(part2) == 8684
