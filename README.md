# NERS570-Sudoku
## Setup
- Make venv `python3 -m venv env`
- Source env `source ./env/bin/activate`
- Verify env `which python`
- Install deps `pip install -r requirements.txt`
- If add new deps make sure to freeze `pip freeze > requirements.txt`

## Class Structure
- Recursive Solver and Humanistic Solvers inherit from the Sudoku base class
  
## How to use
- Instance of the RS or HS using board difficulty and optional id
- Call the solve function