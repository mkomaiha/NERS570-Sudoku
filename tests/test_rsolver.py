from context import RS
import numpy as np
import unittest
from time import time
from random import randint
from parameterized import parameterized
import logging

LOGGER = logging.getLogger(__name__)


class SolveTestSuite(unittest.TestCase):
    """Solve test cases."""

    @ parameterized.expand([
        ("Basic", 0, 5000),
        ("Medium", 1, 5000),
        ("Hard", 2, 5000),
        ("Extreme", 3, 5000),
        ("ExtremeEasy", 3, 1),
        ("ExtremeRandom", 3)
    ])
    def test_solve(self, name, difficulty, boardId=randint(1, 10000)):
        board = RS(difficulty, boardId)
        totalTime = 0
        nRepeats = 1
        for _ in range(nRepeats):
            start = time()
            board.solve()
            totalTime += time() - start
            assert(np.all(board.solved == board.solution))
            board.reset()
        LOGGER.info(f"{name} - {board.difficulty} ({board.boardId})")
        LOGGER.info(f"Elapsed {totalTime/nRepeats}")


if __name__ == '__main__':
    unittest.main()
