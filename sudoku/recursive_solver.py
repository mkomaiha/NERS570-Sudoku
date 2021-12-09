from sudoku.constants import SIZE, BOX_SIZE
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
