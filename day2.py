from itertools import product


def execute_opcode(memory, pc):
    opcode = memory[pc]

    if opcode == 1:
        input1 = memory[pc+1]
        input2 = memory[pc+2]
        output = memory[pc+3]
        memory[output] = memory[input1] + memory[input2]
        return pc+4

    if opcode == 2:
        input1 = memory[pc+1]
        input2 = memory[pc+2]
        output = memory[pc+3]
        memory[output] = memory[input1] * memory[input2]
        return pc+4

    if opcode == 99:
        return -1

    raise Error('Unknown opcode: ' + opcode)


def execute_program(memory_, noun=12, verb=2):
    memory = memory_[::]
    pc = 0

    memory[1] = noun
    memory[2] = verb

    while 0 <= pc <= len(memory):
        pc = execute_opcode(memory, pc)

    return memory[0]


def find_noun_and_verb(memory, expected_output):
    for inputs in product(range(100), repeat=2):
        noun, verb = inputs[0], inputs[1]

        output = execute_program(memory, noun, verb)

        if output == expected_output:
            return noun, verb

    raise Error('No solution !')


data = open('day2.data').read().split(',')
data = map(int, data)
noun, verb = find_noun_and_verb(data, 19690720)

output = 100 * noun + verb
assert(output == 6421)
