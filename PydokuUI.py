import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QStyle
from PyQt6.QtCore import Qt
from PydokuGame import PydokuGame

normal_cell = "background: white; color: black; font-size: 20pt; font-weight: 400; "



class PydokuApp(QWidget):

  def __init__(self):
    super(PydokuApp, self).__init__()
    self.setWindowTitle("Pydoku")
    self.game = PydokuGame()
    self.setup()

  def setup(self):
    main_layout = QVBoxLayout()
    grid_container = QHBoxLayout()
    grid_layout = QGridLayout()

    for row in range(9):
      for col in range(9):
        cell = Cell()
        cell.widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cell.widget.setFixedHeight(32)
        cell.widget.setFixedWidth(32)
        cell.widget.setStyleSheet(normal_cell)
        cell.widget.setInputMask("d")
        if ((row // 3) % 2) + ((col // 3) % 2) == 1:
          cell.widget.setStyleSheet(normal_cell + "background: grey;")
        grid_layout.addWidget(cell.widget, row, col)
        
    solve_button = QPushButton(text="Solve")
    solve_button.clicked.connect(self.solve)

    load_button = QPushButton(text="Load...")
    load_button.clicked.connect(self.load_file)
    
    # set main layout
    self.grid_layout = grid_layout
    grid_container.addLayout(grid_layout)
    main_layout.addLayout(grid_container)
    main_layout.addWidget(load_button)
    main_layout.addWidget(solve_button)
    self.setLayout(main_layout)

  def load_file(self):
    filename, _ = QFileDialog.getOpenFileName(self, "Open file", self.game.game_dir, "Game files (*.pdg)")
    self.game.load(filename)

    for row in range(9):
      for col in range(9):
        cell_value = str(self.game.get_board()[row][col])
        if self.game.get_board()[row][col]:
          self.grid_layout.itemAtPosition(row, col).widget().setStyleSheet(normal_cell + "font-weight: 700;")
          self.grid_layout.itemAtPosition(row, col).widget().setDisabled(True)
        else:
          self.grid_layout.itemAtPosition(row, col).widget().setStyleSheet(normal_cell + "font-weight: 400;")
          self.grid_layout.itemAtPosition(row, col).widget().setDisabled(False)
          
        
    self.update()

  def update(self):
    for row in range(9):
      for col in range(9):
        # set widget at {row}:{col} to board value
        cell_value = str(self.game.get_board()[row][col])
        self.grid_layout.itemAtPosition(row, col).widget().setText(cell_value)


  def solve(self):
    self.game.solve()
    self.update()


class Cell:

  def __init__(self, is_starting_value=False, is_dark:bool=False) -> None:
    self.is_dark = is_dark
    self.is_starting_value = is_starting_value
    normal_style = "background: white; color: black; font-size: 20pt; font-weight: 400; "
    self.widget = QLineEdit()
    self.widget.setStyleSheet(normal_style + "background: grey; " * is_dark)

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = PydokuApp()
  window.show()
  app.exec()