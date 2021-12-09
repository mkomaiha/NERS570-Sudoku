from time import time
from random import randint
import numpy as np


def timedBoardSolve(board, nRepeats=1):
    totalTime = 0
    for _ in range(nRepeats):
        start = time()
        board.solve()
        totalTime += time() - start
        assert(np.all(board.solved == board.solution))
        board.reset()
    print(f"{board.difficulty} ({board.boardId})")
    print(f"Elapsed {totalTime/nRepeats}")


def timedBoardDiffSolve(boardType, boardDiff, nRepeats=1):
    totalTime = 0
    print(f"Timing {boardType.__name__} at difficulty {boardDiff}")
    for _ in range(nRepeats):
        board = boardType(boardDiff)
        start = time()
        board.solve()
        lTime = time() - start
        totalTime += lTime
        print(f"\t{board.difficulty} ({board.boardId}) took {lTime}")
        assert(np.all(board.solved == board.solution))
    print(f"Averaged Time {totalTime/nRepeats}")
