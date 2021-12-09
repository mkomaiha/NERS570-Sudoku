from context import RS
from helpers import timedBoardSolve, timedBoardDiffSolve

for diff in range(4):
    try:
        timedBoardSolve(RS(diff, 11), 10)
    except:
        print(f"Failed difficulty {diff}")

# Times vary a lot w/in difficulty!
for diff in range(4):
    try:
        timedBoardDiffSolve(RS, diff, 10)
    except:
        print(f"Failed difficulty {diff}")
