"""
Opening the front panel reveals a jumble of wires. Specifically, two wires are connected to 
a central port and extend outward on a grid. You trace the path each wire takes as it leaves 
the central port, one wire per line of text (your puzzle input).

The wires twist and turn, but the two wires occasionally cross paths. To fix the circuit, you need 
to find the intersection point closest to the central port. Because the wires are on a grid, 
use the Manhattan distance for this measurement. While the wires do technically cross right at the central port 
where they both start, this point does not count, nor does a wire count as crossing with itself.

For example, if the first wire's path is R8,U5,L5,D3, then starting from the central port (o), 
it goes right 8, up 5, left 5, and finally down 3:

...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........
Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4, and left 4:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........
These wires cross at two locations (marked X), but the lower-left one is closer to the central port: 
its distance is 3 + 3 = 6.

Here are a few more examples:

R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135
What is the Manhattan distance from the central port to the closest intersection?

--- Part Two ---
It turns out that this circuit is very timing-sensitive; you actually need to minimize 
the signal delay.

To do this, calculate the number of steps each wire takes to reach each intersection; 
choose the intersection where the sum of both wires' steps is lowest. If a wire visits
 a position on the grid multiple times, use the steps value from the first time it visits
  that position when calculating the total value of a specific intersection.

The number of steps a wire takes is the total number of grid squares the wire has entered
 to get to that location, including the intersection being considered. Again consider the
  example from above:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........
In the above example, the intersection closest to the central port is reached after 
8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20 steps by the second wire for a 
total of 20+20 = 40 steps.

However, the top-right intersection is better: the first wire takes only 8+5+2 = 15 
and the second wire takes only 7+6+2 = 15, a total of 15+15 = 30 steps.

Here are the best steps for the extra examples from above:

R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps
What is the fewest combined steps the wires must take to reach an intersection?
"""

wire1 = 'R1005,U370,L335,D670,R236,D634,L914,U15,R292,D695,L345,D183,R655,U438,R203,U551,'\
        'L540,U51,R834,D563,L882,D605,L832,U663,R899,D775,L740,U764,L810,U442,R379,D951,'\
        'L821,D703,R526,D624,L100,D796,R375,U129,L957,D41,R361,D504,R358,D320,L392,D842,'\
        'R509,D612,L92,U788,L361,D757,R428,U257,L663,U956,L748,U938,R588,D942,R819,D732,'\
        'R562,D331,L164,U801,R872,U872,L909,U260,R899,D278,R822,U968,L937,D594,L786,D34,'\
        'R102,D650,R920,D539,R925,U436,R347,U686,L596,D608,R730,U5,R462,U831,R277,U411,'\
        'R730,D828,L169,D276,L669,U167,R55,D879,L329,U258,R585,D134,R977,D609,L126,U848,'\
        'L601,U624,R577,D421,L880,D488,R505,U385,L103,D693,L110,D338,R809,D864,L80,U413,'\
        'R412,D134,L519,D988,R83,U580,R593,U435,R843,D953,R11,D655,R569,D237,R987,U894,'\
        'L445,U974,L746,U450,R99,U69,R84,U258,L248,D581,R215,U306,R480,U126,R275,D353,'\
        'R493,D800,L386,D876,L957,D722,L967,D612,L716,D901,R394,U764,R274,D686,L746,D957,'\
        'R747,U517,L575,D961,R842,D753,L345,D59,L215,U413,R610,D166,L646,U107,L926,D848,'\
        'R445,U297,L376,U869,L345,D529,R620,D353,R682,D908,R378,D221,R64,D911,L245,D364,'\
        'R123,D555,L928,U412,R771,D543,L97,D477,R500,D125,R578,U150,R291,D252,R948,D576,'\
        'L838,D144,L289,D677,L307,U692,R802,D743,R57,U839,R896,D110,R34,D508,L595,U658,'\
        'L769,U47,L292,U66,R217,D8,L835,D479,L71,D24,R429,U64,R305,D406,R23,U819,R478,D7,'\
        'L561,D503,R349,U104,L749,D123,R548,D421,R336,D837,R464,D908,L94,U988,L137,D757,'\
        'L42,U842,R260,D406,L31,U965,L178,U973,L29,U276,L887,U920,L133,U243,R537,U282,R194,'\
        'D152,R693,D509,L771,D365,L319,D378,L61,D849,R379'

wire2 = 'L998,U242,R333,U631,L507,U313,R286,U714,R709,U585,R393,D893,R404,D448,R882,U246,'\
        'L190,U238,R672,D184,L275,D120,R352,D584,L626,U413,L288,D942,R770,D551,L926,D242,'\
        'R568,U48,R108,D349,R750,D323,L529,D703,L672,U775,L700,D465,L528,D596,R990,U366,'\
        'L747,D270,L723,D469,L548,D47,L873,D678,R782,D187,L397,U975,R967,D224,L295,D86,'\
        'L159,U610,L767,U641,L885,D623,L160,D509,R517,D981,L376,D604,R251,D140,L938,D358,'\
        'L984,U63,R513,D54,L718,U90,L343,D982,L575,D692,L508,D361,L297,D880,L46,D875,R40,'\
        'D97,R819,U919,R319,U152,R161,U553,L388,D100,R481,U306,L201,U706,L173,D657,L632,'\
        'D182,R477,D332,R678,D683,L983,D584,R941,U801,R485,D376,R218,D432,R780,D617,R560,'\
        'D618,R466,U456,L952,D72,R339,U16,L543,U176,L423,D770,L714,U621,L850,U929,R132,'\
        'D908,R993,U440,R539,U374,L945,D443,L326,D651,L269,U321,R925,D777,R431,U273,R811,'\
        'D63,R683,D540,L3,D617,R359,U332,L736,D98,L859,D994,R131,U71,L156,D661,R879,D303,'\
        'L581,U407,L166,U878,L831,D871,R953,D137,L903,U200,R34,D857,R448,D412,L311,D212,'\
        'R527,D707,R641,D775,L987,D814,L38,D96,R647,U868,L98,U882,L838,D308,R840,U161,R83,'\
        'U424,L420,U934,R353,D287,R559,D665,R695,D888,R859,U992,L283,D525,L449,U255,L889,'\
        'D296,R72,D899,R316,D3,L308,D404,L356,D333,R645,U274,R336,U258,R599,U746,L142,U21,'\
        'R301,D890,L290,D624,R565,U117,L927,U412,L687,U480,R674,U372,L382,D134,L372,D892,'\
        'R307,U217,L20,D535,L876,D548,L19,U590,R906,D816,R465,U768,R882,U980,L557,D788,R645,'\
        'U684,L255,D803,L374,U759,L693,D92,L256,U772,R591,D126,R57,U363,R347,U191,L760,U223,'\
        'R591,D507,R232,U251,R471,D912,R227'

# wire1 = 'R8,U5,L5,D3'
# wire2 = 'U7,R6,D4,L4'

# wire1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'
# wire2 = 'U62,R66,U55,R34,D71,R55,D58,R83'

# wire1 = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'
# wire2 = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'

DX = {'L': -1, 'R': 1, 'U': 0, 'D': 0}
DY = {'L': 0, 'R': 0, 'U': 1, 'D': -1}

def get_points(wire):
    x = 0
    y = 0
    length = 0
    ans = {}
    for cmd in wire:
        d = cmd[0]
        n = int(cmd[1:])
        assert d in 'LRUD'
        for _ in range(n):
            x += DX[d]
            y += DY[d]
            length += 1
            if (x, y) not in ans:
                ans[(x, y)] = length
    return ans

PA = get_points(wire1.split(','))
PB = get_points(wire2.split(','))
both = set(PA.keys()) & set(PB.keys())
part1 = min([abs(x) + abs(y) for (x, y) in both])
part2 = min([PA[p] + PB[p] for p in both])
print(part1)
print(part2)
