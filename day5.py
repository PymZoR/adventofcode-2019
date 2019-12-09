from itertools import product

params_number = dict(zip(
    [1, 2, 3, 4, 5, 6, 7, 8, 99],
    [3, 3, 1, 1, 2, 2, 3, 3, 0])
)


def zero_pad(instruction, length=5):
    zeroes = ''.join(['0' for _ in range(5-len(instruction))])
    return zeroes + instruction


def get_user_input():
    return int(raw_input('>> '))


def execute_instruction(memory, pc):
    instruction = str(memory[pc])
    instruction = zero_pad(instruction)
    opcode = int(instruction[-2:])
    modes = [int(mode) for mode in reversed(instruction[:3])]
    params = [memory[pc+i] for i in range(1, params_number[opcode]+1)]

    assert opcode in [1, 2, 3, 4, 5, 6, 7, 8,  99]

    def get_input():
        mode = modes.pop(0)
        value = params.pop(0)
        return value if mode else memory[value]

    def store(val):
        memory[params.pop(0)] = val

    if opcode == 99:
        return -1

    if opcode == 1:
        input1, input2 = get_input(), get_input()
        store(input1 + input2)

    if opcode == 2:
        input1, input2 = get_input(), get_input()
        store(input1 * input2)

    if opcode == 3:
        input1 = get_user_input()
        store(input1)

    if opcode == 4:
        input1 = get_input()
        print(str(input1))

    if opcode == 5:
        input1, input2 = get_input(), get_input()

        if input1:
            return input2

    if opcode == 6:
        input1, input2 = get_input(), get_input()

        if not input1:
            return input2

    if opcode == 7:
        input1, input2 = get_input(), get_input()
        store(1 if input1 < input2 else 0)

    if opcode == 8:
        input1, input2 = get_input(), get_input()
        store(1 if input1 == input2 else 0)

    return pc + 1 + params_number[opcode]


def execute_program(memory):
    pc = 0

    while 0 <= pc <= len(memory):
        pc = execute_instruction(memory, pc)

    return memory[0]


data = open('day5.data').read().split(',')
data = list(map(int, data))
execute_program(data)

# part 1
# << 1
# >> 7286649

# part 2
# << 5
# >> 15724522
