import requests
import re
from bs4 import BeautifulSoup
from sudoku.constants import BOX_SIZE, SIZE, SUDOKU_API_BASE_URI


def nLoops(loops, start, stop, func, prev):
    for var in range(start, stop):
        cv = [*prev, var]
        if (loops == 1):
            func(cv)
        else:
            nLoops(loops-1, var+1, stop, func, cv)


def getBoxIdxs(r: int, c: int):
    i0 = (r // BOX_SIZE) * BOX_SIZE  # get first row index
    j0 = (c // BOX_SIZE) * BOX_SIZE  # get first column index
    for i in range(i0, i0 + BOX_SIZE):
        for j in range(j0, j0 + BOX_SIZE):
            # if (i != r or j != c):
            yield (i, j)


def boardToString(board):
    output = ''
    for row in board:
        for n in row:
            output += f"{n if n else '.'}"
    return output

# Use Corrected instead
# def stringToBoard(boardStr):
#     board = []
#     inList = []
#     for i, n in enumerate(boardStr):
#         if n == '.':
#             n = 0
#         inList.append(int(n))
#         if (i % 9 == 8):
#             board.append(inList)
#             inList = []
#     return board


# For boardStrings that are cellIdxed i.e.
# 080420050005000362007005000000201500003908000010500000000060000500090400009034000
# [[0,8,0,0,0,5,0,0,7],
#  [4,2,0,0,0,0,0,0,5],
#  [0,5,0,3,6,2,0,0,0],
#  [0,0,0,0,0,3,0,1,0],
#  [2,0,1,9,0,8,5,0,0],
#  [5,0,0,0,0,0,0,0,0],
#  [0,0,0,5,0,0,0,0,9],
#  [0,6,0,0,9,0,0,3,4],
#  [0,0,0,4,0,0,0,0,0]]
def correctCellString(boardStr_):
    nCols = SIZE
    nRows = SIZE
    assert(len(boardStr_) == nCols * nRows)
    board = [[0] * nCols for i in range(nRows)]
    boardStr = ''
    for i in range(nRows):
        for j in range(nCols):
            strIdx = ((i // BOX_SIZE) * nRows + i % BOX_SIZE) * BOX_SIZE + \
                (j // BOX_SIZE) * nCols + j % BOX_SIZE
            numStr = boardStr_[strIdx]
            boardStr += '.' if numStr == '0' else numStr
            num = 0 if numStr == '.' else int(numStr)
            board[i][j] = num
    return board, boardStr


def getBoard(grade=0, id=None):
    difficulty = [
        {'btdebutant': 'Beginner'},
        {'btconfirme': 'Confirmed'},
        {'btexpert': 'Expert'},
        {'btextreme': 'Extreme'}]
    assert grade < len(
        difficulty), f'Grade must be < {len(difficulty)}. Idx in {difficulty}'
    data = difficulty[grade]
    if (not (id is None)):
        data = {
            'SelectNiveau': grade + 1,
            'TextNum': id,
            'Com': 'btnumero'
        }
    board_data = {'board': [], 'difficulty': '', 'solution': []}
    r = requests.post(
        'https://www.sudoku-puzzles-online.com/sudoku/enter-a-solution-sudoku.php', data=data)
    # Cell string board
    soup = BeautifulSoup(r.text, 'html.parser')
    boardStrCell = soup.find('input', attrs={'name': 'Eno'}).get('value')
    boardId = int(soup.find('input', attrs={'name': 'TextNum'}).get('value'))
    boardGrade = int(soup.find(
        'input', attrs={'name': 'SelectNiveau'}).get('value'))
    assert boardGrade == grade + 1, 'Returned grade not the same as requested!'

    # Convert to board and corrected cell str (row major)
    board, boardStr = correctCellString(boardStrCell)
    board_data = {
        'board': board,
        'boardStr': boardStr,
        'boardId': boardId
    }

    # Verify uniqueness
    boardTest = requests.get(
        f"https://www.thonky.com/sudoku/solution-count?puzzle={boardToString(board_data['board'])}").text
    nSolutions = int(re.search(
        'Number of solutions: ([0-9]+)', boardTest).group(1))
    assert nSolutions == 1, 'No unique solution!'
    # TODO: Use the above api for the solution instead of the one below

    # Get solution
    data = {
        'board': str(board_data['board'])
    }
    solve_data = requests.post(
        f'{SUDOKU_API_BASE_URI}/solve', data=data).json()
    board_data.update(solve_data)
    board_data['est_difficulty'] = board_data['difficulty']
    board_data['difficulty'] = list(difficulty[grade].values())[0]
    return board_data

# Are not validating
# def validateBoard(board):
#     data = {
#         'board': str(board)
#     }
#     validated = requests.post(
#         f'{SUDOKU_API_BASE_URI}/validate', data=data).json()
#     # 'unsolved', 'broken', 'solved'
#     return validated['status']
