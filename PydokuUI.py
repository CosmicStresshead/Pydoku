import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from PydokuGame import PydokuGame

class PydokuApp(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Pydoku")
    self.game = PydokuGame()
    self.setup()

  def setup(self):
    main_layout = QVBoxLayout()
    grid_container = QHBoxLayout()
    grid_layout = QGridLayout()

    self.game.load("1")

    for row in range(9):
      for col in range(9):
        cell_value = str(self.game.get_board()[row][col])
        cell = QLineEdit()
        cell.setText(cell_value)
        # set size
        cell.setFixedHeight(32)
        cell.setFixedWidth(32)
        # set style
        cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_weight = "400"
        font_size = "20pt"
        if int(cell_value) in range(1, 10):
          cell.setDisabled(True)
          font_weight = "700"
        # set rules
        cell.setMaxLength(1)
        cell.setInputMask("d")
        # format grid appearance
        if (row // 3 in [0, 2] and col // 3 in [0, 2]) or (row // 3 == 1 and col // 3 == 1):
          cell_background = "white"
        else:
          cell_background = "grey"
        cell.setStyleSheet(f"background: {cell_background}; color: black; font-weight: {font_weight}; font-size: {font_size}")
        # add to layout
        grid_layout.addWidget(cell, row, col)
        
    solve_button = QPushButton(text="Solve")
    solve_button.clicked.connect(self.solve)
    
    # set main layout
    self.grid_layout = grid_layout
    grid_container.addLayout(grid_layout)
    main_layout.addLayout(grid_container)
    main_layout.addWidget(solve_button)
    self.setLayout(main_layout)

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