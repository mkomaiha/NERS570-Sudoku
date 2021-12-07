from context import recursiveSolver as rs
import numpy as np
import unittest
from time import time

class SolveTestSuite(unittest.TestCase):
    """Solve test cases."""

    def test_basic_solve(self):
        board = rs.RS(0, 300)
        t0 = time()
        board.recursive_solver()
        print("Elapsed time:",time()-t0)
        #assert(np.all(board.solved == board.solution))

    def test_medium_solve(self):
        board = rs.RS(1, 4000)
        t0 = time()
        board.recursive_solver()
        print("Elapsed time:",time()-t0)
        #assert(np.all(board.solved == board.solution))


    def test_hard_solve(self):
        board = rs.RS(2, 10000)
        t0 = time()
        board.recursive_solver()
        print("Elapsed time:",time()-t0)
        #assert(np.all(board.solved == board.solution))


    def test_extreme_solve(self):
        board = rs.RS(3, 40000)
        t0 = time()
        board.recursive_solver()
        print("Elapsed time:",time()-t0)
        #assert(np.all(board.solved == board.solution))


if __name__ == '__main__':
    unittest.main()



