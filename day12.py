import re
from itertools import combinations
from collections import defaultdict
from copy import deepcopy
from functools import reduce
from math import gcd

data = open('day12.data').read().splitlines()

# Parse planets positions
planets = defaultdict(lambda: {"pos": [0, 0, 0], "vel": [0, 0, 0]})
for i, line in enumerate(data):
    pos_vector = re.findall(r'(\w)=(-?\d+)', line)

    for j, axis in enumerate(pos_vector):
        _, value = axis
        planets[i]["pos"][j] = int(value)

# Simulation
pairs = list(combinations(planets.keys(), 2))

for t in range(1000):
    for pair in pairs:
        planet1 = planets[pair[0]]
        planet2 = planets[pair[1]]

        # For each axis
        for i in range(3):
            # Update velocity
            if planet1["pos"][i] > planet2["pos"][i]:
                planet2["vel"][i] += 1
                planet1["vel"][i] -= 1

            if planet2["pos"][i] > planet1["pos"][i]:
                planet1["vel"][i] += 1
                planet2["vel"][i] -= 1

    # Update position
    for planet in planets.values():
        for i in range(3):
            planet["pos"][i] += planet["vel"][i]

part1 = sum((sum(map(abs, planet["vel"])) * sum(map(abs, planet["pos"]))
             for planet in planets.values()))

assert(part1 == 9139)


def lcm(a, b):
    return abs(a*b) // gcd(a, b)


# Parse planets positions
planets = defaultdict(lambda: {"pos": [0, 0, 0], "vel": [0, 0, 0]})
for i, line in enumerate(data):
    pos_vector = re.findall(r'(\w)=(-?\d+)', line)

    for j, axis in enumerate(pos_vector):
        _, value = axis
        planets[i]["pos"][j] = int(value)

# Copy initial state
initial_planets = deepcopy(planets)

frequencies = [-1, -1, -1]
t = 0
while -1 in frequencies:
    t += 1
    for pair in pairs:
        planet1 = planets[pair[0]]
        planet2 = planets[pair[1]]

        # For each axis
        for i in range(3):
            # Update velocity
            if planet1["pos"][i] > planet2["pos"][i]:
                planet2["vel"][i] += 1
                planet1["vel"][i] -= 1

            if planet2["pos"][i] > planet1["pos"][i]:
                planet1["vel"][i] += 1
                planet2["vel"][i] -= 1

    # Update position
    for i, planet in planets.items():
        for j in range(3):
            planet["pos"][j] += planet["vel"][j]

    # Find if axis is back to original state
    for j in range(3):
        frequencyFound = True
        for i, planet in planets.items():
            if planet["pos"][j] != initial_planets[i]["pos"][j] or planet["vel"][j] != 0:
                frequencyFound = False

        if frequencyFound and frequencies[j] == -1:
            frequencies[j] = t


part2 = reduce(lcm, frequencies)
assert(part2 == 420788524631496)
