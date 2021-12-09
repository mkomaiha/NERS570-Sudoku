from copy import deepcopy
from typing import List, Tuple, Set
from sudoku.helpers import getBoard, validateBoard, boardToString, getBoxIdxs, nLoops
from sudoku.constants import BOX_SIZE, SIZE
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

        self.solved = np.copy(self.board)
        self.possibilities = np.ones(
            (*np.shape(self.board), SIZE), dtype=int)  # Use bool instead?

    def __repr__(self) -> str:
        out = f'Sudoku {self.difficulty} no {self.boardId} ({self.est_difficulty})\nBoard:\n'
        out += str(self.board) + '\n'
        out += f'Board str: {self.boardStr}\n'
        out += 'Solution:\n'
        out += str(self.solution) + '\n'
        return out

    def reset(self):
        self.solved = self.board
        self.possibilities = np.ones(
            (*np.shape(self.board), SIZE), dtype=int)
