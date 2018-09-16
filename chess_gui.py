from board import Board
from AI import AI
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette

WIDTH = 540
HEIGHT = 540
COUNT = 15
MARGIN = 22
PIECE = 34
GRID = (WIDTH - 2 * MARGIN) / (15 - 1)
EMPTY = 0
BLACK = 1
WHITE = 2


class ChessGui(QWidget):
    def __init__(self):
        super().__init__()
        self.ai = AI()
        self.init_ui()
        self.current_color = BLACK

    def init_ui(self):
        self.chessboard = Board()

        windows_pale = QPalette()
        windows_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("chessboard.jpg")))
        self.setPalette(windows_pale)

        self.resize(WIDTH, HEIGHT)
        self.setMinimumSize(QtCore.QSize(WIDTH, HEIGHT))
        self.setMaximumSize(QtCore.QSize(WIDTH, HEIGHT))

        self.setWindowTitle("chess")
        self.black = QPixmap("black.png")
        self.white = QPixmap("white.png")

        self.current_color = BLACK
        self.player_first = True
        self.step = 0
        self.pieces = [QLabel(self) for i in range(COUNT * COUNT)]
        for item in self.pieces:
            item.setVisible(True)
            item.setScaledContents(True)
        """
        self.mouse_point = QLabel(self)
        self.mouse_point.raise_()
        self.setMouseTracking(True)
        """
        self.setMouseTracking(True)
        self.show()
        print("init success")

    def draw(self, x_0, y_0):
        x, y = self.transfer_board_to_widget(x_0, y_0)
        if self.current_color == BLACK:
            self.pieces[self.step].setPixmap(QPixmap('black.png'))
            self.current_color = WHITE
            self.chessboard.set_at_xy(x_0, y_0, BLACK)
        else:
            self.pieces[self.step].setPixmap(QPixmap('white.png'))
            self.current_color = BLACK
            self.chessboard.set_at_xy(x_0, y_0, WHITE)

        self.pieces[self.step].setGeometry(y, x, PIECE, PIECE)
        self.step += 1

    def transfer_widget_to_board(self, x, y):
        x_1, y_1 = int(round((x - MARGIN) / GRID)), int(round((y - MARGIN) / GRID))
        if x_1 >= 0 and x_1 < 15 and y_1 >= 0 and y_1 < 15:
            return x_1, y_1
        else:
            return None, None

    def transfer_board_to_widget(self, x, y):
        return MARGIN + x * GRID - PIECE / 2, MARGIN + y * GRID - PIECE / 2

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            y, x = e.x(), e.y()
            x_board, y_board = self.transfer_widget_to_board(x, y)
            if x_board is not None and y_board is not None and self.chessboard.get_xy_color(x_board, y_board) is EMPTY:
                self.draw(x_board, y_board)
                if self.chessboard.is_win(x_board, y_board) is True:
                    QMessageBox.information(self, "result", "You Win! Press to quit.", QMessageBox.Yes)
                    sys.exit(0)

                self.ai.upgrade(self.chessboard, x_board, y_board)
                x_ai, y_ai = self.ai.calculate(self.player_first)
                self.draw(x_ai, y_ai)
                if self.chessboard.is_win(x_ai, y_ai) is True:
                    QMessageBox.information(self, "result", "You Lose! Press to quit.", QMessageBox.Yes)
                    sys.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChessGui()
    sys.exit(app.exec_())
