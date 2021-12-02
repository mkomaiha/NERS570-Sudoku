import sudoku as s

b1 = s.Sudoku(0,1)
b2 = s.Sudoku(1,2)
b3 = s.Sudoku(2,3)
b4 = s.Sudoku(3,4)

b1.recursive_solver()
b2.recursive_solver()
b3.recursive_solver()
b4.recursive_solver()

