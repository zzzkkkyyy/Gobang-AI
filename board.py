class Board(object):
    length = 15
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    direct = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]

    def __init__(self):
        self.board = [[self.EMPTY for i in range(self.length)] for j in range(self.length)]

    def get_board(self):
        return self.board

    def judge_if_out(self, x, y):
        if x >= 0 and x < self.length and y >= 0 and y < self.length:
            return True
        return False

    def set_at_xy(self, x, y, color):
        if self.judge_if_out(x, y) is True:
            self.board[x][y] = color

    def get_xy_color(self, x, y):
        return self.board[x][y]

    def get_neighbor_xy(self, x, y, direction):
        x_n = x + direction[0]
        y_n = y + direction[1]
        if self.judge_if_out(x_n, y_n):
            return x_n, y_n
        return None, None

    def is_win(self, x, y):
        color = self.get_xy_color(x, y)
        for index in range(4):
            flag = True
            x_n, y_n = x, y
            while self.get_xy_color(x_n, y_n) is color:
                x_temp, y_temp = self.get_neighbor_xy(x_n, y_n, self.direct[index])
                if x_temp is None:
                    break
                else:
                    x_n, y_n = x_temp, y_temp

            if flag is True:
                for i in range(5):
                    x_n, y_n = self.get_neighbor_xy(x_n, y_n, self.direct[index + 4])
                    if x_n is None or self.get_xy_color(x_n, y_n) != color:
                        flag = False
                        break

            if flag is True:
                return True
            else:
                continue
        return False

