from copy import deepcopy
from typing import List, Tuple, Set
from helpers import getBoard, validateBoard, boardToString
import time
import numpy as np
from sudoku import Sudoku

class RS(Sudoku):
    def __init__(self, grade=0, id=None):
        board = getBoard(grade, id)
        self.board = board['board']
        self.boardStr = board['boardStr']
        self.boardId = board['boardId']
        self.solution = board['solution']
        self.difficulty = board['difficulty']
        self.est_difficulty = board['est_difficulty']
        self.grid = self.board
        self.n = len(self.grid)
        
    def possible(self,r,c,n):
        for i in range(0,self.SIZE):
             if self.grid[r][i] == n:
                 return False
        for i in range(0,self.SIZE):
             if self.grid[i][c] == n:
                 return False
        c0 = (c//self.BOX_SIZE)*self.BOX_SIZE;
        r0 = (r//self.BOX_SIZE)*self.BOX_SIZE;
        for i in range(0,self.BOX_SIZE):
             for j in range(0, self.BOX_SIZE):
                 if self.grid[r0+i][c0+j] == n:
                     return False
        return True

    def recursive_solver(self,printflag = False):
       # t = time.time()
        for r in range(self.SIZE):
             for c in range(self.SIZE):
                 if self.grid[r][c] == 0:
                     for n in range(1,10):
                         if self.possible(r,c,n):
                             self.grid[r][c] = n
                             self.recursive_solver()
                             self.grid[r][c] = 0
                     return
      #  print('Elapsed: %s' % (time.time() - t))
        if printflag == True:
            print('recursive results:')
            print(np.matrix(self.grid))
        self.checksoln()

    def checksoln(self):
        check = True
    #    for r in range(SIZE):
    #         for c in range(SIZE):
        if self.grid!= self.solution:
              check = False
        if check == True:
             print("all correct!")
        else:
             print("something is wrong...")
        return check
 

    def candidates(self):
         # create a grid of viable candidates for each position
        candidates = []
        for i in range(self.n):
             row = []
             for j in range(self.n):
                 if self.grid[i][j] == 0:
                     row.append(self.find_options(i, j))
                 else:
                     row.append(set())
             candidates.append(row)
        self.candidates = candidates
        return self.candidates

    def __repr__(self) -> str:
        repr = f'Sudoku {self.difficulty} no {self.boardId} ({self.est_difficulty})\nBoard:\n'
        for row in self.board:
            repr += str(row) + '\n'
        repr += f'Board str: {self.boardStr}\n'
        repr += 'Solution:\n'
        for row in self.solution:
            repr += str(row) + '\n'
        return repr

    def get_row(self, r: int) -> List[int]:
         return self.grid[r]

    def get_col(self, c: int) -> List[int]:
         return [row[c] for row in self.grid]

    def get_box_inds(self, r: int, c: int) -> List[Tuple[int,int]]:
         inds_box = []
         i0 = (r // BOX_SIZE) * BOX_SIZE  # get first row index
         j0 = (c // BOX_SIZE) * BOX_SIZE  # get first column index
         for i in range(i0, i0 + BOX_SIZE):
             for j in range(j0, j0 + BOX_SIZE):
                 inds_box.append((i, j))
         return inds_box

    def get_box(self, r: int, c: int) -> List[int]:
         box = []
         for i, j in self.get_box_inds(r, c):
             box.append(self.grid[i][j])
         return box

    def find_options(self, r: int, c: int) -> Set:
        nums = set(range(1, SIZE + 1))
        set_row = set(self.get_row(r))
        set_col = set(self.get_col(c))
        set_box = set(self.get_box(r, c))
        used = set_row | set_col | set_box
        valid = nums.difference(used)
        return valid
