from context import HS
import numpy as np
from time import time
import unittest
from parameterized import parameterized
from random import randint
import logging

LOGGER = logging.getLogger(__name__)


class SolveTestSuite(unittest.TestCase):
    """Solve test cases."""
    @parameterized.expand([
        ("Basic", 0, 3),
        ("Medium", 1, 8000),
        ("Hard", 2, 9999),
        ("Extreme", 3, 10000),
        ("ExtremeEasy", 3, 1),
        ("ExtremeRandom", 3)
    ])
    def test_solve(self, name, difficulty, boardId=randint(1, 10000)):
        board = HS(difficulty, boardId)
        totalTime = 0
        nRepeats = 10
        for i in range(nRepeats):
            start = time()
            board.solve()
            totalTime += time() - start
            assert(np.all(board.solved == board.solution))
            board.reset()
        LOGGER.info(f"{name} - {board.difficulty} ({board.boardId})")
        LOGGER.info(f"Elapsed {totalTime/nRepeats}")


if __name__ == '__main__':
    unittest.main()
