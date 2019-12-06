from itertools import product


def zero_pad(instruction, length=5):
    zeroes = ''.join(['0' for _ in range(5-len(instruction))])
    return zeroes + instruction


def execute_instruction(memory, pc):
    def get_value(mode, value):
        return value if mode else memory[value]

    instruction = str(memory[pc])
    instruction = zero_pad(instruction)
    opcode = int(instruction[-2:])
    modes = [int(mode) for mode in reversed(instruction[:3])]

    assert opcode in [1, 2, 3, 4, 5, 6, 7, 8,  99]

    if opcode == 99:
        return -1

    if opcode == 1:
        args = [memory[pc+i] for i in range(1, 3+1)]
        input1 = get_value(modes[0], args[0])
        input2 = get_value(modes[1], args[1])
        output = args[2]
        memory[output] = input1 + input2
        return pc+4

    if opcode == 2:
        args = [memory[pc+i] for i in range(1, 3+1)]
        input1 = get_value(modes[0], args[0])
        input2 = get_value(modes[1], args[1])
        output = args[2]
        memory[output] = input1 * input2
        return pc+4

    if opcode == 3:
        args = [memory[pc+i] for i in range(1, 1+1)]
        user_input = raw_input('>> ')
        input1 = int(user_input)
        input2 = args[0]
        memory[input2] = input1
        return pc+2

    if opcode == 4:
        args = [memory[pc+i] for i in range(1, 1+1)]
        input1 = get_value(modes[0], args[0])
        print(str(input1))
        return pc + 2

    if opcode == 5:
        args = [memory[pc+i] for i in range(1, 2+1)]
        input1 = get_value(modes[0], args[0])
        input2 = get_value(modes[1], args[1])

        if input1:
            return input2

        return pc + 3

    if opcode == 6:
        args = [memory[pc+i] for i in range(1, 2+1)]
        input1 = get_value(modes[0], args[0])
        input2 = get_value(modes[1], args[1])

        if not input1:
            return input2

        return pc + 3

    if opcode == 7:
        args = [memory[pc+i] for i in range(1, 3+1)]
        input1 = get_value(modes[0], args[0])
        input2 = get_value(modes[1], args[1])
        input3 = args[2]
        memory[input3] = 1 if input1 < input2 else 0

        return pc + 4

    if opcode == 8:
        args = [memory[pc+i] for i in range(1, 3+1)]
        input1 = get_value(modes[0], args[0])
        input2 = get_value(modes[1], args[1])
        input3 = args[2]
        memory[input3] = 1 if input1 == input2 else 0

        return pc + 4


def execute_program(memory):
    pc = 0

    while 0 <= pc <= len(memory):
        pc = execute_instruction(memory, pc)

    return memory[0]


data = open('day5.data').read().split(',')
data = list(map(int, data))
execute_program(data)
