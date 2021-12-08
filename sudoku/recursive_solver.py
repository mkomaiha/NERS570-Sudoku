from typing import List, Tuple, Set
from sudoku.constants import SIZE, BOX_SIZE
from sudoku.helpers import getBoard, validateBoard, boardToString
from sudoku import Sudoku


class RS(Sudoku):
    def __init__(self, grade=0, id=None):
        super().__init__(grade, id)

    def possible(self, r, c, n):
        for i in range(0, SIZE):
            if self.solved[r, i] == n:
                return False
        for i in range(0, SIZE):
            if self.solved[i, c] == n:
                return False
        c0 = (c//BOX_SIZE)*BOX_SIZE
        r0 = (r//BOX_SIZE)*BOX_SIZE
        for i in range(0, BOX_SIZE):
            for j in range(0, BOX_SIZE):
                if self.solved[r0+i, c0+j] == n:
                    return False
        return True

    def r_solve(self, printflag=False):
        for r in range(SIZE):
            for c in range(SIZE):
                if self.solved[r, c] == 0:
                    for n in range(1, 10):
                        if self.possible(r, c, n):
                            self.solved[r, c] = n
                            # Prevent from reseting the board
                            if (self.r_solve(printflag)):
                                return True
                            self.solved[r, c] = 0
                    return False

        if printflag == True:
            print('recursive results:')
            print(self.solved)
        return True

    def solve(self, printflag=False):
        self.r_solve(printflag)
        return self.solved

    def candidates(self):
        # create a solved of viable candidates for each position
        candidates = []
        for i in range(SIZE):
            row = []
            for j in range(SIZE):
                if self.solved[i, j] == 0:
                    row.append(self.find_options(i, j))
                else:
                    row.append(set())
            candidates.append(row)
        return candidates

    def get_row(self, r: int) -> List[int]:
        return self.solved[r]

    def get_col(self, c: int) -> List[int]:
        return [row[c] for row in self.solved]

    def get_box_inds(self, r: int, c: int) -> List[Tuple[int, int]]:
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
            box.append(self.solved[i, j])
        return box

    def find_options(self, r: int, c: int) -> Set:
        nums = set(range(1, SIZE + 1))
        set_row = set(self.get_row(r))
        set_col = set(self.get_col(c))
        set_box = set(self.get_box(r, c))
        used = set_row | set_col | set_box
        valid = nums.difference(used)
        return valid
