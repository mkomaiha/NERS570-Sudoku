from context import sudoku

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_constructor(self):
        board = sudoku.Sudoku()
        assert(hasattr(board, "board"))
        assert(hasattr(board, "boardStr"))
        assert(hasattr(board, "boardId"))
        assert(hasattr(board, "solution"))
        assert(hasattr(board, "difficulty"))
        assert(hasattr(board, "est_difficulty"))

    def test_difficulty(self):
        board = sudoku.Sudoku(0)
        assert(board.difficulty == 'Beginner')
        board = sudoku.Sudoku(1)
        assert(board.difficulty == 'Confirmed')
        board = sudoku.Sudoku(2)
        assert(board.difficulty == 'Expert')
        board = sudoku.Sudoku(3)
        assert(board.difficulty == 'Extreme')

    def test_specific_board(self):
        board = sudoku.Sudoku(0, 1)
        assert(board.difficulty == 'Beginner')
        assert(board.boardId == 1)
        assert(board.boardStr ==
               '.....1.32..5.239.4..96....7.5.1...7....3..2...6..8..5.3..2.64856.........9473.6..')
        board = sudoku.Sudoku(1, 999)
        assert(board.difficulty == 'Confirmed')
        assert(board.boardId == 999)
        assert(board.boardStr ==
               '.......96..96..5.83........4.5..7....2.9..645.........75..1.8....34.89..6........')


if __name__ == '__main__':
    unittest.main()
