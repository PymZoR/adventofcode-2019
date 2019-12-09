from itertools import product, permutations

params_number = dict(zip(
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 99],
    [3, 3, 1, 1, 2, 2, 3, 3, 1, 0])
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
        self.memory = memory + [0 for _ in range(10000)]
        self.pc = 0
        self.base = 0

    def execute_instruction(self):
        instruction = str(self.memory[self.pc])
        instruction = zero_pad(instruction)
        opcode = int(instruction[-2:])
        modes = [int(mode) for mode in reversed(instruction[:3])]
        params = [self.memory[self.pc+i]
                  for i in range(1, params_number[opcode]+1)]

        assert opcode in [1, 2, 3, 4, 5, 6, 7, 8, 9, 99]

        def get_input():
            mode = modes.pop(0)
            value = params.pop(0)

            assert mode in [0, 1, 2]

            if mode == 0:
                return self.memory[value]
            elif mode == 1:
                return value
            elif mode == 2:
                return self.memory[self.base + value]

        def store(val):
            mode = modes.pop(0)
            if mode == 0:
                self.memory[params.pop(0)] = val
            else:
                self.memory[self.base + params.pop(0)] = val

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
            print(instruction)
            try:
                input1 = self.inputs.pop(0)
                print("GET <<", input1)
                store(input1)
            except Exception:
                return RET_CODE['WAIT_INPUT']

        if opcode == 4:
            input1 = get_input()
            self.outputs.append(input1)

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

        if opcode == 9:
            input1 = get_input()
            self.base += input1

        self.pc += params_number[opcode] + 1

    def run(self):
        while 0 <= self.pc <= len(self.memory):
            ret_code = self.execute_instruction()

            if ret_code is not None:
                return ret_code


# Read program
data = open('day9.data').read().split(',')
data = list(map(int, data))

machine = IntCodeMachine(data)
machine.inputs.append(2)
ret = machine.run()
print(machine.outputs)
