"""
--- Day 9: Sensor Boost ---
You've just said goodbye to the rebooted rover and left Mars when you receive a faint 
distress signal coming from the asteroid belt. It must be the Ceres monitoring station!

In order to lock on to the signal, you'll need to boost your sensors. The Elves send up the 
latest BOOST program - Basic Operation Of System Test.

While BOOST (your puzzle input) is capable of boosting your sensors, for tenuous safety 
reasons, it refuses to do so until the computer it runs on passes some checks to 
demonstrate it is a complete Intcode computer.

Your existing Intcode computer is missing one key feature: it needs support for parameters 
in relative mode.

Parameters in mode 2, relative mode, behave very similarly to parameters in position mode: 
the parameter is interpreted as a position. Like position mode, parameters in relative 
mode can be read from or written to.

The important difference is that relative mode parameters don't count from address 0. 
Instead, they count from a value called the relative base. The relative base starts at 0.

The address a relative mode parameter refers to is itself plus the current relative base. 
When the relative base is 0, relative mode parameters and position mode parameters with 
the same value refer to the same address.

For example, given a relative base of 50, a relative mode parameter of -7 refers to memory 
address 50 + -7 = 43.

The relative base is modified with the relative base offset instruction:

Opcode 9 adjusts the relative base by the value of its only parameter. The relative base 
increases (or decreases, if the value is negative) by the value of the parameter.
For example, if the relative base is 2000, then after the instruction 109,19, the relative 
base would be 2019. If the next instruction were 204,-34, then the value at address 1985 
would be output.

Your Intcode computer will also need a few other capabilities:

The computer's available memory should be much larger than the initial program. Memory 
beyond the initial program starts with the value 0 and can be read or written like any 
other memory. (It is invalid to try to access memory at a negative address, though.)
The computer should have support for large numbers. Some instructions near the beginning 
of the BOOST program will verify this capability.
Here are some example programs that use these features:

109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99 takes no input and produces a 
copy of itself as output.
1102,34915192,34915192,7,4,7,99,0 should output a 16-digit number.
104,1125899906842624,99 should output the large number in the middle.
The BOOST program will ask for a single input; run it in test mode by providing it 
the value 1. It will perform a series of checks on each opcode, output any opcodes 
(and the associated parameter modes) that seem to be functioning incorrectly, and 
finally output a BOOST keycode.

Once your Intcode computer is fully functional, the BOOST program should report no 
malfunctioning opcodes when run in test mode; it should only output a single value, 
the BOOST keycode. What BOOST keycode does it produce?

--- Part Two ---
You now have a complete Intcode computer.

Finally, you can lock on to the Ceres distress signal! You just need to boost your 
sensors using the BOOST program.

The program runs in sensor boost mode by providing the input instruction the value 2. 
Once run, it will boost the sensors automatically, but it might take a few seconds to 
complete the operation on slower hardware. In sensor boost mode, the program will 
output a single value: the coordinates of the distress signal.

Run the BOOST program in sensor boost mode. What are the coordinates of the distress signal?
"""
POSITION = 0
IMMEDIATE = 1
RELATIVE = 2

ADD = 1
MUL = 2
IN = 3
OUT = 4
JUMP_TRUE = 5
JUMP_FALSE = 6
LESS_THAN = 7
EQUALS = 8
ADD_RELATIVE_BASE = 9
HALT = 99

READ = 0
WRITE = 1

OPS = {
    ADD: (READ, READ, WRITE),
    MUL: (READ, READ, WRITE),
    IN: (WRITE,),
    OUT: (READ,),
    JUMP_TRUE: (READ, READ),
    JUMP_FALSE: (READ, READ),
    LESS_THAN: (READ, READ, WRITE),
    EQUALS: (READ, READ, WRITE),
    ADD_RELATIVE_BASE: (READ,),
    HALT: (),
}


class VM:
    def __init__(self, code, inp):
        self.code = list(code)
        self.inp = inp

    def __getitem__(self, index):
        return self.mem[index]

    def __setitem__(self, index, val):
        self.mem[index] = val

    def get_args(self, arg_kinds, modes):
        args = [None] * 4

        for i, kind in enumerate(arg_kinds):
            a = self[self.ip + 1 + i]
            mode = modes % 10
            modes //= 10

            if mode == RELATIVE:
                a += self.relative_base

            if mode in (POSITION, RELATIVE):
                if a < 0:
                    raise Exception(f"Invalid access to negative memory index: {a}")
                elif a >= len(self.mem):
                    self.mem += [0] * (a + 1 - len(self.mem))

                if kind == READ:
                    a = self[a]
                elif kind != WRITE:
                    raise Exception(f"Invalid arg kind: {kind}")

            elif mode == IMMEDIATE:
                if kind == WRITE:
                    raise Exception(f"Invalid arg mode for write arg: {mode}")
            else:
                raise Exception(f"Invalid arg mode: {mode}")

            args[i] = a

        return args

    def run(self):
        self.ip = 0
        self.relative_base = 0
        self.mem = self.code.copy()
        out = None

        while self[self.ip] != HALT:
            instr = self[self.ip]
            op = instr % 100
            modes = instr // 100

            if op not in OPS:
                raise Exception(f"Unknown opcode: {op}")

            arg_kinds = OPS[op]
            a, b, c, d = self.get_args(arg_kinds, modes)
            self.ip += 1 + len(arg_kinds)

            if op == IN:
                self[a] = self.inp
            elif op == OUT:
                out = a
            elif op == ADD:
                self[c] = a + b
            elif op == MUL:
                self[c] = a * b
            elif op == LESS_THAN:
                self[c] = 1 if a < b else 0
            elif op == EQUALS:
                self[c] = 1 if a == b else 0
            elif op == JUMP_TRUE:
                if a != 0:
                    self.ip = b
            elif op == JUMP_FALSE:
                if a == 0:
                    self.ip = b
            elif op == ADD_RELATIVE_BASE:
                self.relative_base += a
            else:
                raise Exception(f"Unimplemented opcode: {op}")

        return out


with open('input/day9.txt') as f:
    code = list(map(int, f.readline().strip().split(",")))

    print('Part 1:', VM(code, 1).run())
    print('Part 2:', VM(code, 2).run())
