from math import floor


def get_fuel_from_mass(mass):
    if mass <= 0:
        return 0

    current_fuel = floor(mass/3) - 2
    fuel_list = []

    while current_fuel > 0:
        fuel_list.append(current_fuel)
        current_fuel = floor(current_fuel/3) - 2

    return int(sum(fuel_list))


def get_fuel_from_modules(module_list):
    return int(sum(map(get_fuel_from_mass, module_list)))


data = open('./day1.data').read().split()
data = map(int, data)

output = get_fuel_from_modules(data)
assert(output == 4816402)
