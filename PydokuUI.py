import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QStyle
from PyQt6.QtCore import Qt
from PydokuGame import PydokuGame

stylesheets = dict()

stylesheets["normal_cell"] = "background: white; color: black; font-size: 20pt; font-weight: 400"
stylesheets["prefilled_normal_cell"] = "background: white; color: black; font-size: 20pt; font-weight: 700"
stylesheets["normal_cell_dark"] = "background: grey; color: black; font-size: 20pt; font-weight: 400"
stylesheets["prefilled_cell_dark"] = "background: grey; color: black; font-size: 20pt; font-weight: 700"



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
        cell = QLineEdit()
        cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cell.setFixedHeight(32)
        cell.setFixedWidth(32)
        cell.setStyleSheet(stylesheets["normal_cell_dark"])
        if (row//3 in [0, 2] and col//3 in [0, 2]) or (row//3 == 1 and col//3 == 1):
          cell.setStyleSheet(stylesheets["normal_cell"])

        grid_layout.addWidget(cell, row, col)
        
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


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = PydokuApp()
  window.show()
  app.exec()