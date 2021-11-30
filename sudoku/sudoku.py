from copy import deepcopy
from typing import List, Tuple, Set
from .helpers import getBoard, validateBoard, boardToString


class Sudoku():
    def __init__(self, grade=0, id=None):
        board = getBoard(grade, id)
        self.board = board['board']
        self.boardStr = board['boardStr']
        self.boardId = board['boardId']
        self.solution = board['solution']
        self.difficulty = board['difficulty']
        self.est_difficulty = board['est_difficulty']
        # n = len(grid)
        # self.grid = grid
        # self.n = n
        # # create a grid of viable candidates for each position
        # candidates = []
        # for i in range(n):
        #     row = []
        #     for j in range(n):
        #         if grid[i][j] == 0:
        #             row.append(self.find_options(i, j))
        #         else:
        #             row.append(set())
        #     candidates.append(row)
        # self.candidates = candidates

    def __repr__(self) -> str:
        repr = f'Sudoku {self.difficulty} no {self.boardId} ({self.est_difficulty})\nBoard:\n'
        for row in self.board:
            repr += str(row) + '\n'
        repr += f'Board str: {self.boardStr}\n'
        repr += 'Solution:\n'
        for row in self.solution:
            repr += str(row) + '\n'
        return repr

    # def get_row(self, r: int) -> List[int]:
    #     return self.grid[r]

    # def get_col(self, c: int) -> List[int]:
    #     return [row[c] for row in self.grid]

    # def get_box_inds(self, r: int, c: int) -> List[Tuple[int,int]]:
    #     inds_box = []
    #     i0 = (r // BOX_SIZE) * BOX_SIZE  # get first row index
    #     j0 = (c // BOX_SIZE) * BOX_SIZE  # get first column index
    #     for i in range(i0, i0 + BOX_SIZE):
    #         for j in range(j0, j0 + BOX_SIZE):
    #             inds_box.append((i, j))
    #     return inds_box

    # def get_box(self, r: int, c: int) -> List[int]:
    #     box = []
    #     for i, j in self.get_box_inds(r, c):
    #         box.append(self.grid[i][j])
    #     return box
