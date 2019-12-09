from itertools import product, permutations

params_number = dict(zip(
    [1, 2, 3, 4, 5, 6, 7, 8, 99],
    [3, 3, 1, 1, 2, 2, 3, 3, 0])
)

RET_CODE = dict(zip(
    ['HALT', 'WAIT_INPUT'],
    [0, 1]
))


def zero_pad(instruction, length=5):
    zeroes = ''.join(['0' for _ in range(5-len(instruction))])
    return zeroes + instruction


class IntCodeMachine:
    def __init__(self, memory=[]):
        self.inputs = []
        self.outputs = []

        self.reset(memory)

    def reset(self, memory):
        self.memory = memory
        self.pc = 0

    def execute_instruction(self):
        instruction = str(self.memory[self.pc])
        instruction = zero_pad(instruction)
        opcode = int(instruction[-2:])
        modes = [int(mode) for mode in reversed(instruction[:3])]
        params = [self.memory[self.pc+i]
                  for i in range(1, params_number[opcode]+1)]

        assert opcode in [1, 2, 3, 4, 5, 6, 7, 8,  99]

        def get_input():
            mode = modes.pop(0)
            value = params.pop(0)
            return value if mode else self.memory[value]

        def store(val):
            self.memory[params.pop(0)] = val

        if opcode == 99:
            self.pc = -1

            return RET_CODE['HALT']

        if opcode == 1:
            input1, input2 = get_input(), get_input()
            store(input1 + input2)

        if opcode == 2:
            input1, input2 = get_input(), get_input()
            store(input1 * input2)

        if opcode == 3:
            try:
                input1 = self.inputs.pop(0)
                # print("GET <<", input1)
                store(input1)
            except Exception:
                return RET_CODE['WAIT_INPUT']

        if opcode == 4:
            input1 = get_input()
            self.outputs.append(input1)
            # print("OUT >>", input1)

        if opcode == 5:
            input1, input2 = get_input(), get_input()

            if input1:
                self.pc = input2
                return

        if opcode == 6:
            input1, input2 = get_input(), get_input()

            if not input1:
                self.pc = input2
                return

        if opcode == 7:
            input1, input2 = get_input(), get_input()
            store(1 if input1 < input2 else 0)

        if opcode == 8:
            input1, input2 = get_input(), get_input()
            store(1 if input1 == input2 else 0)

        self.pc += params_number[opcode] + 1

    def run(self):
        while 0 <= self.pc <= len(self.memory):
            ret_code = self.execute_instruction()

            if ret_code is not None:
                return ret_code


# Read program
data = open('day7.data').read().split(',')
data = list(map(int, data))

# Create amplifiers
amplifiers = [IntCodeMachine() for _ in range(5)]

# Link amplifiers input / output
for i in range(1, 5):
    # Link next amplifier input to current amplifier output
    amplifiers[i].inputs = amplifiers[i-1].outputs

# Test combinations
max_output = -1
for comb in permutations(range(5), 5):
    for i in range(5):
        # Reset amplifier
        amplifiers[i].reset(data)
        # Phase settings is first input
        amplifiers[i].inputs.insert(0, comb[i])

        # First amplifier needs manual 0 input
        if i == 0:
            amplifiers[0].inputs.append(0)

        # Run program
        ret = amplifiers[i].run()

    # Store max output signal
    output = amplifiers[-1].outputs.pop(0)
    if output > max_output:
        max_output = output

part1 = max_output
assert(part1 == 21000)

# PART 2


# Link last amplifier output to first amplifier inpout
amplifiers[0].inputs = amplifiers[4].outputs

max_output = -1
for comb in permutations(range(5, 10), 5):
    # Reset amplifiers
    for i in range(5):
        amplifiers[i].reset(data)
        # Phase settings is first input
        amplifiers[i].inputs.append(comb[i])

    # First amplifier needs manual 0 input
    amplifiers[0].inputs.append(0)

    ret = None
    while not ret == RET_CODE['HALT']:
        for i in range(5):
            # Run program
            ret = amplifiers[i].run()

    # Store max output signal
    output = amplifiers[-1].outputs.pop(0)
    if output > max_output:
        max_output = output

part2 = max_output
assert(part2 == 61379886)
