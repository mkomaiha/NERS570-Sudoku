from sudoku.helpers import getBoxIdxs, nLoops
from sudoku.constants import BOX_SIZE, SIZE
import numpy as np
from sudoku import Sudoku


class HS(Sudoku):
    def __init__(self, grade=0, id=None):
        super().__init__(grade, id)

    def update_solution(self, row, col, valIdx):
        # Thread Lock
        self.solved[row, col] = valIdx + 1
        print(f"Setting ({row}, {col}) to {valIdx+1}")
        self.updatePossib(row, col, valIdx)

    def elimination(self):
        # Elimination over all the BOXES
        changes = 0
        for box in range(SIZE):
            print("Elimination on box", box)
            for idx in range(SIZE):
                row = (idx // BOX_SIZE) + (box // BOX_SIZE) * BOX_SIZE
                col = (idx % BOX_SIZE) + (box % BOX_SIZE) * BOX_SIZE
                if (self.solved[row, col]):
                    continue
                possible = np.nonzero(self.possibilities[row, col])[0]
                # Backtrack if no possible?
                if (len(possible) == 1):
                    valIdx = possible[0]
                    print(f"Found elimination {valIdx + 1} at ({row}, {col})")
                    self.update_solution(row, col, valIdx)
                    changes += 1
        return changes > 0

    def loneranger(self):
        changes = 0
        # Lone ranger over all the BOXES
        for box in range(SIZE):
            print("Lone ranger checking box", box)
            i0 = (box // BOX_SIZE) * BOX_SIZE
            j0 = (box % BOX_SIZE) * BOX_SIZE
            possOccurances = np.sum(
                self.possibilities[i0:i0+BOX_SIZE,
                                   j0:j0+BOX_SIZE], axis=(1, 0)) == 1
            possible = np.nonzero(possOccurances)[0]
            for valIdx in possible:
                boolWhere = self.possibilities[i0:i0+BOX_SIZE,
                                               j0:j0+BOX_SIZE,
                                               valIdx] == 1
                idxOfWhere = np.asarray(np.where(boolWhere)).T + [i0, j0]
                row, col = idxOfWhere[0]
                print(f"Found LR {valIdx + 1} at ({row}, {col})")
                self.update_solution(row, col, valIdx)
                changes += 1
            if box in [1, 2, 4]:
                for j in range(j0, j0+BOX_SIZE):
                    print("Lone ranger checking columns", j)
                    possOccurances = np.sum(
                        self.possibilities[:, j], axis=(0,)) == 1
                    possible = np.nonzero(possOccurances)[0]
                    for valIdx in possible:
                        boolWhere = self.possibilities[:, j, valIdx] == 1
                        row = np.asarray(np.where(boolWhere)).T[0, 0]
                        print(f"Found LR {valIdx + 1} at ({row}, {j})")
                        self.update_solution(row, j, valIdx)
                        changes += 1
            elif box in [0, 5, 6]:
                for i in range(i0, i0+BOX_SIZE):
                    print("Lone ranger checking rows", i)
                    possOccurances = np.sum(
                        self.possibilities[i, :], axis=(0,)) == 1
                    possible = np.nonzero(possOccurances)[0]
                    for valIdx in possible:
                        boolWhere = self.possibilities[i, :, valIdx] == 1
                        col = np.asarray(np.where(boolWhere)).T[0, 0]
                        print(f"Found LR {valIdx + 1} at ({i}, {col})")
                        self.update_solution(i, col, valIdx)
                        changes += 1
        return changes > 0

    def findSame(self, countSame=2):
        changes = 0
        # Lone ranger over all the BOXES
        for box in range(SIZE):
            print(f"{countSame} of same checking box", box)
            i0 = (box // BOX_SIZE) * BOX_SIZE
            j0 = (box % BOX_SIZE) * BOX_SIZE
            shift = [i0, j0]
            flip = False
            roi = self.possibilities[i0:i0+BOX_SIZE,
                                     j0:j0+BOX_SIZE]

            def doStuff(vals):
                nonlocal changes
                mask = np.zeros((SIZE, 1), dtype=int)
                mask[vals] = 1
                masked = roi @ mask
                if (len(np.shape(masked)) > 2):
                    masked = np.squeeze(masked, axis=-1)
                boolWhere = masked == countSame
                if (flip):
                    boolWhere = boolWhere.T
                idxOfWhere = np.asarray(np.where(boolWhere)).T + shift
                # Assumes elimination runs first, shouldn't find
                # naked singles
                if (len(idxOfWhere) == countSame and not np.any((masked < countSame) & (masked > 0))):
                    found = 0
                    for (row, col) in idxOfWhere:
                        # No changes
                        if (np.sum(self.possibilities[row, col]) == countSame):
                            continue
                        # TODO: Change this to set to 0 isntead that way even if
                        # two threads try to change it is okay bc will both change to 0
                        # no methods bring a possibility back to 1
                        self.possibilities[row, col] = (
                            self.possibilities[row, col] & mask.T)[0]
                        found += 1
                    if (found):
                        print(self.solved)
                        print(
                            f"Found {len(vals)} of same {np.array(vals)+1} at {[list(loc) for loc in idxOfWhere]}")
                    changes += found
            nLoops(countSame, 0, SIZE, doStuff, [])
            # Gain any thing from this??
            if box in [1, 2, 4]:
                for j in range(j0, j0+BOX_SIZE):
                    shift = [0, j]
                    print(f"{countSame} of same checking column", j)
                    roi = self.possibilities[:, j]
                    nLoops(countSame, 0, SIZE, doStuff, [])
            elif box in [0, 5, 6]:
                flip = True
                for i in range(i0, i0+BOX_SIZE):
                    shift = [i, 0]
                    print(f"{countSame} of same checking row", i)
                    roi = self.possibilities[i, :]
                    nLoops(countSame, 0, SIZE, doStuff, [])
        return changes > 0

    def twins(self):
        return self.findSame(2)

    def triples(self):
        return self.findSame(3)

    def updatePossib(self, row, col, valIdx):
        self.possibilities[row, col, :] = 0
        # self.possibilities[row, col, valIdx] = 1
        for (r, c) in getBoxIdxs(row, col):
            self.possibilities[r, c, valIdx] = 0
        for i in range(SIZE):
            #     if i == row:
            #         continue
            self.possibilities[i, col, valIdx] = 0
        for j in range(SIZE):
            #     if i == col:
            #         continue
            self.possibilities[row, j, valIdx] = 0

    def solve(self):
        # Update possibilities for initial board
        for row in range(SIZE):
            for col in range(SIZE):
                val = self.solved[row, col]
                if (val != 0):
                    self.updatePossib(row, col, val-1)
        total = SIZE**2
        # TODO: IMPLEMENT MORE STRATEGIES LIKE TWINS AND TRIPLES
        strategies = [self.elimination, self.loneranger,
                      self.twins, self.triples]
        while (np.count_nonzero(self.solved) < total):
            for strategy in strategies:
                if strategy():
                    break
            else:
                print("stuck!")
                break
        print(self.solved)
        print(self.solution)
        print(self.solved == self.solution)
        print(np.count_nonzero(self.solved))
