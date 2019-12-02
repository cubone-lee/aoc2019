"""
Fuel required to launch a given module is based on its mass. Specifically, 
to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

For example:

For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
For a mass of 1969, the fuel required is 654.
For a mass of 100756, the fuel required is 33583.
The Fuel Counter-Upper needs to know the total fuel requirement. To find it, 
individually calculate the fuel needed for the mass of each module (your puzzle input), 
then add together all the fuel values.

What is the sum of the fuel requirements for all of the modules on your spacecraft?

--- Part Two ---

Fuel itself requires fuel just like a module - take its mass, divide by three, round down, and subtract 2.
However, that fuel also requires fuel, and that fuel requires fuel, and so on. 
Any mass that would require negative fuel should instead be treated as if it requires zero fuel; 
the remaining mass, if any, is instead handled by wishing really hard, which has no mass and 
is outside the scope of this calculation.

So, for each module mass, calculate its fuel and add it to the total. Then, treat the fuel amount you just 
calculated as the input mass and repeat the process, continuing until a fuel requirement is zero or negative. 
For example:

A module of mass 14 requires 2 fuel. This fuel requires no further fuel (2 divided by 3 and rounded down is 0, 
which would call for a negative fuel), so the total fuel required is still just 2.
At first, a module of mass 1969 requires 654 fuel. Then, this fuel requires 216 more fuel (654 / 3 - 2). 
216 then requires 70 more fuel, which requires 21 fuel, which requires 5 fuel, which requires no further fuel. 
So, the total fuel required for a module of mass 1969 is 654 + 216 + 70 + 21 + 5 = 966.
The fuel required by a module of mass 100756 and its fuel is: 33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346.
What is the sum of the fuel requirements for all of the modules on your spacecraft when also taking into account 
the mass of the added fuel? (Calculate the fuel requirements for each module separately, then add them all 
up at the end.)
"""

import math

puzzle_input ="""
125050
115884
132344
67441
119823
86204
111093
99489
67860
51288
62815
65263
56540
81380
96101
116351
56330
123123
133969
115050
137851
136900
71254
53458
139976
140218
117085
52241
71251
136110
103784
132893
140216
85568
94327
85200
136753
110917
147197
120161
81684
56987
143452
94728
138355
54577
59898
69123
133769
118418
93530
50297
71543
113383
135203
140129
70977
58566
129593
137456
130100
130915
88872
96014
62746
127048
89522
62021
85363
143611
135995
65836
146022
119911
127381
121007
71577
129637
90271
54640
117213
116151
114022
107683
102079
94388
135676
69019
104056
124799
107998
148696
122793
135417
52981
122890
142491
88137
57609
54921
"""

result_p1 = 0

def cal_fuel(puzzle):
    return math.floor(int(puzzle) / 3) - 2

for puzzle in puzzle_input.splitlines():
    if not puzzle:
        continue
    result_p1 += cal_fuel(puzzle)
print('>>>RESULT P1: {}'.format(result_p1))

result_p2 = 0
for puzzle in puzzle_input.splitlines():
    if not puzzle:
        continue
    fuel = cal_fuel(puzzle)
    result_p2 += fuel
    while fuel > 0:
        fuel = cal_fuel(fuel)
        if fuel < 1:
            continue
        result_p2 += fuel
print('>>>RESULT P2: {}'.format(result_p2))
