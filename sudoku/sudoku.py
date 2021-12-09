from sudoku.helpers import getBoard
from sudoku.constants import SIZE
import numpy as np


class Sudoku():
    def __init__(self, grade=0, id=None):
        board = getBoard(grade, id)
        self.board = np.array(board['board'])
        self.boardStr = board['boardStr']
        self.boardId = board['boardId']
        self.solution = np.array(board['solution'])
        self.difficulty = board['difficulty']
        self.est_difficulty = board['est_difficulty']
        self.reset()

    def __repr__(self) -> str:
        out = f'Sudoku {self.difficulty} no {self.boardId} ({self.est_difficulty})\nBoard:\n'
        out += str(self.board) + '\n'
        out += f'Board str: {self.boardStr}\n'
        out += 'Solution:\n'
        out += str(self.solution) + '\n'
        return out

    def reset(self):
        self.solved = np.copy(self.board)
        self.possibilities = np.ones(
            (*np.shape(self.board), SIZE), dtype=int)  # Use bool instead?
