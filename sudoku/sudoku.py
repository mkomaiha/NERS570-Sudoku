from copy import deepcopy
from typing import List, Tuple, Set
from .helpers import getBoard, validateBoard, boardToString, getBoxIdxs
from .constants import BOX_SIZE, SIZE
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

    def update_solution(self, row, col, valIdx):
        # Thread Lock
        self.solved[row, col] = valIdx + 1
        self.updatePossib(row, col, valIdx)

    def elimination(self):
        # Elimination over all the BOXES
        changes = 0
        for box in range(SIZE):
            for idx in range(SIZE):
                row = (idx // BOX_SIZE) + (box // BOX_SIZE) * BOX_SIZE
                col = (idx % BOX_SIZE) + (box % BOX_SIZE) * BOX_SIZE
                if (self.solved[row, col]):
                    break
                possible = np.nonzero(self.possibilities[row, col])[0]
                # Backtrack if no possible?
                if (len(possible) == 1):
                    valIdx = possible[0]
                    print(f"Found {valIdx + 1} at ({row}, {col})")
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
                print(f"Found {valIdx + 1} at ({row}, {col})")
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
                        print(f"Found {valIdx + 1} at ({row}, {j})")
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
                        print(f"Found {valIdx + 1} at ({i}, {col})")
                        self.update_solution(i, col, valIdx)
                        changes += 1

        return changes > 0

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
        strategies = [self.elimination, self.loneranger]
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

        #     if(!changed) {
        #     #pragma omp parallel for schedule(dynamic)
        #     for(int thread_id = 0; thread_id < board->dim; thread_id++) {
        #         #pragma omp atomic update
        #         changed |= twins(thread_id, ROW);
        #         #pragma omp atomic update
        #         changed |= twins(thread_id, COL);
        #         #pragma omp atomic update
        #         changed |= twins(thread_id, BLOCK);
        #     }
        #     }

        #     if(!changed) {
        #     #pragma omp parallel for
        #     for(int thread_id = 0; thread_id < board->dim; thread_id++) {
        #         #pragma omp atomic update
        #         changed |= triplets(thread_id, ROW);
        #         #pragma omp atomic update
        #         changed |= triplets(thread_id, COL);
        #         #pragma omp atomic update
        #         changed |= triplets(thread_id, BLOCK);
        #     }
        #     }

        #     if(!changed) {
        #     make_guess();
        #     }
        # }
        # }
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
