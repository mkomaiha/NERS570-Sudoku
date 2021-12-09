from context import HS
from helpers import timedBoardSolve, timedBoardDiffSolve

for diff in range(4):
    timedBoardSolve(HS(diff, 11), 1)

# Times vary a lot w/in difficulty!
for diff in range(4):
    timedBoardDiffSolve(HS, diff, 5)
