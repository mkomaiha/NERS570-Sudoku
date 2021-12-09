from context import RS
from helpers import timedBoardSolve, timedBoardDiffSolve

for diff in range(4):
    timedBoardSolve(RS(diff, 9999), 1)

# Times vary a lot w/in difficulty!
for diff in range(4):
    timedBoardDiffSolve(RS, diff, 5)
