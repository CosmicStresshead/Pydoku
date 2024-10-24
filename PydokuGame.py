from os import path

class PydokuGame:

  def __init__(self):
    self._board = [[0] * 9] * 9
    self.game_dir = "puzzles"

  def get_board(self) -> None:
    return self._board
  
  def set_board(self, value_array: list) -> None:
    if self.validate_data(value_array):
      self._board = value_array

  def load(self, filepath: str) -> bool:
    data = []
    # read file
    with open(filepath, "r") as f:
      for i in range(9):
        try:
          data.append([int(c) for c in f.readline()[:9]])
        except Exception as e:
          print(f"ERROR: Could not load from file: {e}")
          return False
    # validate
    if not self.validate_data(data):
      return False
    # if valid, set board values and return True
    self._board = data
    return True
  
  def validate_data(self, data: list) -> bool:
    # validate data
    if len(data) != 9:
      return False
    for line in data:
      if len(line) != 9:
        return False
      for value in line:
        if not value in range(0, 10):
          return False
    return True

  def print(self) -> None:
    for row in self._board:
        print(" ".join(map(str, row)))

  def get_board(self):
    return self._board

  def get_row(self, index: int) -> list:
    return self._board[index]
  
  def get_column(self, index: int) -> list:
    column = []
    for row in range(9):
      column.append(self._board[row][index])
    return column
  
  def get_subgrid(self, row: int, col: int) -> list:
    values = []
    row_start = row * 3
    row_end = (row * 3) + 3
    col_start = col * 3
    col_end = (col * 3) + 3
    for row in range(row_start, row_end):
      for col in range(col_start, col_end):
        values.append(self._board[row][col])
    return values

  def validate_no_duplicates(self, values):
    vals = [c for c in values if c.isdigit()]
    if len(values) == len(set(values)):
      return True
    return False
  
  def validate_board(self) -> bool:
    # validate rows & columns
    for i in range(9):
      if not self.validate_no_duplicates(self.get_row(i)):
        return False
      if not self.validate_no_duplicates(self.get_column(i)):
        return False
    
    # validate 3x3 subgrids
    for r in range(3):
      for c in range(3):
        if not self.validate_no_duplicates(self.get_subgrid(r, c)):
          return False
        
    return True
  
  def is_valid(self, row: int, col: int, val: int) -> bool:
    current = self._board[row][col]
    sub_col = col // 3
    sub_row = row // 3
    # compile set of all values, except current value
    all = set(self.get_row(row) + self.get_column(col) + self.get_subgrid(sub_row, sub_col)) - set([current])
    return val not in all

  def solve(self, r: int=0, c:int=0) -> bool:
    ''' Solves the puzzle using backtracking algorithm '''
    # if all rows completed, job done
    if r == 9:
      return True
    elif c == 9:
      # if all columns completed in current row, solve next row
      return self.solve(r+1, 0)
    # skip pre-filled values
    elif self._board[r][c] != 0:
      return self.solve(r, c+1)
    else:
      # try a valid value and move on until solved
      for val in range(1, 10):
        if self.is_valid(r, c, val):
          self._board[r][c] = val
          if self.solve(r, c+1):
            return True
          self._board[r][c] = 0
      # return to starting point to try next value
      return False
    

# if __name__ == "__main__":
#   g = PydokuGame()
#   g.load("2.pdg")
#   # g.solve()
#   g.print()