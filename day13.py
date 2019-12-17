# coding: utf-8

from collections import defaultdict
from itertools import product, permutations
import time

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
            try:
                input1 = self.inputs.pop(0)
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


TILE_TO_CHAR = dict(zip(range(5), [" ", "░", "█", "―", "⏺"]))


def print_screen(instructions):
    screen = defaultdict(lambda: 0)
    width, height = 0, 0
    score = 0
    paddle_pos = None
    ball_pos = None

    for i in range(0, len(instructions), 3):
        x, y, tile_type = instructions[i:i+3]

        if (x, y) == (-1, 0):
            score = tile_type
            continue

        screen[(x, y)] = tile_type
        if x > width:
            width = x
        if y > height:
            height = y

        if tile_type == 3:
            paddle_pos = [x, y]
        if tile_type == 4:
            ball_pos = [x, y]

    for j in range(height):
        line = ""
        for i in range(width):
            tile_type = screen[(i, j)]
            line += TILE_TO_CHAR[tile_type]
        print(line)

    print("score: " + str(score))

    return screen, paddle_pos, ball_pos


# Read program
data = open('day13.data').read().split(',')
data = list(map(int, data))

machine = IntCodeMachine(data)
ret = machine.run()

instructions = list(machine.outputs)
screen, _, _ = print_screen(instructions)
part1 = len(filter(lambda tile: tile == 2, screen.values()))
assert(part1 == 329)


# part 2
print(data[0])
data[0] = 2
print(data[0])
machine.reset(data)

ret_code = -1
while ret_code != RET_CODE['HALT']:
    ret_code = machine.run()
    screen, paddle_pos, ball_pos = print_screen(machine.outputs)

    paddle_pos_x, paddle_pos_y = paddle_pos
    ball_pos_x, ball_pos_y = ball_pos

    if paddle_pos_x < ball_pos_x:
        machine.inputs.append(1)
    elif paddle_pos_x > ball_pos_x:
        machine.inputs.append(-1)
    else:
        machine.inputs.append(0)
