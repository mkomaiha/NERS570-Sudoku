from context import sudoku
import numpy as np
import unittest


class SolveTestSuite(unittest.TestCase):
    """Solve test cases."""

    def test_basic_solve(self):
        board = sudoku.Sudoku(0, 3)
        board.solve()
        assert(np.all(board.solved == board.solution))

    def test_medium_solve(self):
        board = sudoku.Sudoku(1, 4)
        board.solve()
        assert(np.all(board.solved == board.solution))


if __name__ == '__main__':
    unittest.main()
