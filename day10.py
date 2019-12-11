from math import atan2, pi
from itertools import permutations, combinations
from collections import defaultdict


def normalize_angle(angle):
    if angle < 0:
        angle += 2*pi

    return angle % (2*pi)


data = open('day10.data').read().splitlines()
asteroids = {}
for j, line in enumerate(data):
    for i, char in enumerate(line):
        if char == '#':
            asteroids[(i, j)] = []

# for pair in combinations(asteroids.keys(), 2):
for pair in permutations(asteroids.keys(), 2):
    x1, y1 = pair[0]
    x2, y2 = pair[1]
    dy = y2 - y1
    dx = x2 - x1

    angle = normalize_angle(atan2(dy, dx) + (pi/2))
    # angle_reverse = normalize_angle(angle + pi)
    dist = abs(dx) + abs(dy)

    asteroids[pair[0]].append((angle, dist, pair[1]))
    # asteroids[pair[1]].append((angle_reverse, dist))

asteroids_in_view = [(len(set([pair[0] for pair in val])), key)
                     for key, val in asteroids.items()]
best_asteroid = max(asteroids_in_view)
part1 = best_asteroid[0]
assert (part1 == 329)

origin = best_asteroid[1]
los = defaultdict(list)
# (dist, coordinates) for asteroids visible from origin by angle
for asteroid in asteroids[origin]:
    los[asteroid[0]].append(asteroid[1:])

# sort by distance
los = {key: sorted(value) for key, value in los.items()}

vaporized = []
for angle in sorted(los.keys()):
    if len(los[angle]):
        vaporized.append(los[angle].pop(0)[1])

part2 = vaporized[199][0]*100 + vaporized[199][1]
assert (part2 == 512)
