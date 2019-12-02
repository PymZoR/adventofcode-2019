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
    return int(sum([get_fuel_from_mass(mass) for mass in module_list]))


with open("./day1.data", "r") as data:
    data = [int(i) for i in data.read().split()]

    output = get_fuel_from_modules(data)
    assert(output == 4816402)
