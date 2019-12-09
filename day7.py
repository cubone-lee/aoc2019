"""
Based on the navigational maps, you're going to need to send more power to your ship's 
thrusters to reach Santa in time. To do this, you'll need to configure a series of 
amplifiers already installed on the ship.

There are five amplifiers connected in series; each one receives an input signal and 
produces an output signal. They are connected such that the first amplifier's output 
leads to the second amplifier's input, the second amplifier's output leads to the third 
amplifier's input, and so on. The first amplifier's input value is 0, and the last 
amplifier's output leads to your ship's thrusters.

    O-------O  O-------O  O-------O  O-------O  O-------O
0 ->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-> (to thrusters)
    O-------O  O-------O  O-------O  O-------O  O-------O
The Elves have sent you some Amplifier Controller Software (your puzzle input), a program 
that should run on your existing Intcode computer. Each amplifier will need to run a copy 
of the program.

When a copy of the program starts running on an amplifier, it will first use an input 
instruction to ask the amplifier for its current phase setting (an integer from 0 to 4). 
Each phase setting is used exactly once, but the Elves can't remember which amplifier needs 
which phase setting.

The program will then call another input instruction to get the amplifier's input signal, 
compute the correct output signal, and supply it back to the amplifier with an output 
instruction. (If the amplifier has not yet received an input signal, it waits until one 
arrives.)

Your job is to find the largest output signal that can be sent to the thrusters by trying 
every possible combination of phase settings on the amplifiers. Make sure that memory is 
not shared or reused between copies of the program.

For example, suppose you want to try the phase setting sequence 3,1,2,4,0, which would mean 
setting amplifier A to phase setting 3, amplifier B to setting 1, C to 2, D to 4, and E to 0. 
Then, you could determine the output signal that gets sent from amplifier E to the thrusters 
with the following steps:

Start the copy of the amplifier controller software that will run on amplifier A. At its 
first input instruction, provide it the amplifier's phase setting, 3. At its second input 
instruction, provide it the input signal, 0. After some calculations, it will use an output 
instruction to indicate the amplifier's output signal.
Start the software for amplifier B. Provide it the phase setting (1) and then whatever 
output signal was produced from amplifier A. It will then produce a new output signal 
destined for amplifier C.
Start the software for amplifier C, provide the phase setting (2) and the value from 
amplifier B, then collect its output signal.
Run amplifier D's software, provide the phase setting (4) and input value, and collect 
its output signal.
Run amplifier E's software, provide the phase setting (0) and input value, and collect 
its output signal.
The final output signal from amplifier E would be sent to the thrusters. However, this 
phase setting sequence may not have been the best one; another sequence might have sent 
a higher signal to the thrusters.

Here are some example programs:

Max thruster signal 43210 (from phase setting sequence 4,3,2,1,0):

3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
Max thruster signal 54321 (from phase setting sequence 0,1,2,3,4):

3,23,3,24,1002,24,10,24,1002,23,-1,23,
101,5,23,23,1,24,23,23,4,23,99,0,0
Max thruster signal 65210 (from phase setting sequence 1,0,4,3,2):

3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0
Try every combination of phase settings on the amplifiers. What is the highest signal 
that can be sent to the thrusters?

--- Part Two ---
It's no good - in this configuration, the amplifiers can't generate a large enough output 
signal to produce the thrust you'll need. The Elves quickly talk you through rewiring the 
amplifiers into a feedback loop:

      O-------O  O-------O  O-------O  O-------O  O-------O
0 -+->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-.
   |  O-------O  O-------O  O-------O  O-------O  O-------O |
   |                                                        |
   '--------------------------------------------------------+
                                                            |
                                                            v
                                                     (to thrusters)
Most of the amplifiers are connected as they were before; amplifier A's output is connected 
to amplifier B's input, and so on. However, the output from amplifier E is now connected 
into amplifier A's input. This creates the feedback loop: the signal will be sent through 
the amplifiers many times.

In feedback loop mode, the amplifiers need totally different phase settings: integers 
from 5 to 9, again each used exactly once. These settings will cause the Amplifier 
Controller Software to repeatedly take input and produce output many times before halting. 
Provide each amplifier its phase setting at its first input instruction; all further 
input/output instructions are for signals.

Don't restart the Amplifier Controller Software on any amplifier during this process. 
Each one should continue receiving and sending signals until it halts.

All signals sent or received in this process will be between pairs of amplifiers except 
the very first signal and the very last signal. To start the process, a 0 signal is sent 
to amplifier A's input exactly once.

Eventually, the software on the amplifiers will halt after they have processed the final 
loop. When this happens, the last output signal from amplifier E is sent to the thrusters. 
Your job is to find the largest output signal that can be sent to the thrusters using the 
new phase settings and feedback loop arrangement.

Here are some example programs:

Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):

3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):

3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
Try every combination of the new phase settings on the amplifier feedback loop. What is 
the highest signal that can be sent to the thrusters?
"""
from itertools import permutations

with open('input/day7.txt', 'r') as challenge_input:
    thrusters = challenge_input.read()

def get_permutations(li):
    for permutation in permutations(li):
        yield permutation

def get_modes(modes):
    return [int(mode) for mode in [modes[2], modes[1], modes[0], modes[3:]]]


class Computer:
    def __init__(self, data):
        self.idx = 0
        self.data = data[:]
        self.done = False
        self.output = None
        self.inputs = []

    def get_params(self, mode1, mode2):
        return self.get_param(mode1, 1), self.get_param(mode2, 2)

    def get_param(self, mode, increment):
        if mode == 0:
            return self.data[self.data[self.idx + increment]]
        return self.data[self.idx + increment]

    def add(self, param1, param2):
        return param1 + param2

    def multiply(self, param1, param2):
        return param1 * param2

    def less_than(self, param1, param2):
        return 1 if param1 < param2 else 0

    def equals(self, param1, param2):
        return 1 if param1 == param2 else 0

    def jump_if_true(self, mode1, mode2):
        param1, param2 = self.get_params(mode1, mode2)
        return param2 if param1 != 0 else self.idx + 3

    def jump_if_false(self, mode1, mode2):
        param1, param2 = self.get_params(mode1, mode2)
        return param2 if param1 == 0 else self.idx + 3

    def calculate(self, input_val):
        self.inputs.append(input_val)
        while True:
            mode1, mode2, mode3, opcode = get_modes(f"{self.data[self.idx]:05}")
            if opcode == 1:
                param1, param2 = self.get_params(mode1, mode2)
                self.data[self.data[self.idx + 3]] = self.add(param1, param2)
                self.idx += 4
            elif opcode == 2:
                param1, param2 = self.get_params(mode1, mode2)
                self.data[self.data[self.idx + 3]] = self.multiply(param1, param2)
                self.idx += 4
            elif opcode == 3:
                self.data[self.data[self.idx + 1]] = self.inputs.pop(0)
                self.idx += 2
            elif opcode == 4:
                self.output = self.data[self.data[self.idx + 1]]
                self.idx += 2
                return self.output
            elif opcode == 5:
                self.idx = self.jump_if_true(mode1, mode2)
            elif opcode == 6:
                self.idx = self.jump_if_false(mode1, mode2)
            elif opcode == 7:
                param1, param2 = self.get_params(mode1, mode2)
                self.data[self.data[self.idx + 3]] = self.less_than(param1, param2)
                self.idx += 4
            elif opcode == 8:
                param1, param2 = self.get_params(mode1, mode2)
                self.data[self.data[self.idx + 3]] = self.equals(param1, param2)
                self.idx += 4
            elif opcode == 99:
                self.done = True
                return self.output


with open("input/day7.txt") as _file:
    for line in _file:
        input_vals = [int(num) for num in line.split(",")]
        max_output_signal = 0
        for permutation in get_permutations([0, 1, 2, 3, 4]):
            output_signal = 0
            for input_signal in permutation:
                computer = Computer(input_vals[:])
                computer.inputs.append(input_signal)
                output_signal = computer.calculate(output_signal)
            max_output_signal = max(max_output_signal, output_signal)
        print(f"Part 1: {max_output_signal}")

        max_output_signal_2 = 0
        for permutation in get_permutations([5, 6, 7, 8, 9]):
            computers = [Computer(input_vals[:]) for _ in range(5)]
            output_signal = 0
            for computer, phase_setting in zip(computers, permutation):
                computer.inputs.append(phase_setting)
            while computers[-1].done == False:
                for computer in computers:
                    output_signal = computer.calculate(output_signal)
            max_output_signal_2 = max(output_signal, max_output_signal_2)
        print(f"Part 2: {max_output_signal_2}")

