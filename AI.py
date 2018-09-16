from board import Board

class AI:
    shape_score = {}
    list_1 = []
    list_2 = []
    list_3 = []

    list_all = []
    next_pt = [0, 0]

    ratio = 0.1
    depth = 3
    length = 15

    def __init__(self):
        self.board = None
        self.current_x = 0
        self.current_y = 0
        self.current_color = 0

        self.list_1 = []
        self.list_2 = []
        self.list_3 = []
        self.list_all = []
        self.search_begin_index = 0
        self.search_begin_index_before = []
        for i in range(self.length):
            for j in range(self.length):
                self.list_all.append([i, j])

        self.all_score_shape = []

        self.shape_score[(0, 1, 0, 0, 0)] = 10
        self.shape_score[(0, 1, 1, 0, 0)] = 10
        self.shape_score[(0, 0, 1, 1, 0)] = 10
        self.shape_score[(0, 1, 0, 1, 0)] = 10

        self.shape_score[(1, 1, 0, 1, 0)] = 500
        self.shape_score[(0, 1, 0, 1, 1)] = 500
        self.shape_score[(0, 1, 1, 1, 2)] = 5000
        self.shape_score[(2, 1, 1, 1, 0)] = 5000
        self.shape_score[(0, 1, 1, 1, 0)] = 5000
        self.shape_score[(1, 2, 2, 2, 0)] = 50000
        self.shape_score[(0, 2, 2, 2, 1)] = 50000

        self.shape_score[(0, 1, 0, 1, 1, 0)] = 5000
        self.shape_score[(0, 1, 1, 0, 1, 0)] = 5000
        self.shape_score[(1, 1, 1, 0, 1)] = 50000
        self.shape_score[(1, 1, 0, 1, 1)] = 50000
        self.shape_score[(1, 0, 1, 1, 1)] = 50000

        self.shape_score[(1, 1, 1, 1, 0)] = 50000
        self.shape_score[(0, 1, 1, 1, 1)] = 50000
        self.shape_score[(1, 2, 2, 2, 2, 1)] = 500001
        self.shape_score[(2, 1, 1, 1, 1, 2)] = 500001
        self.shape_score[(0, 1, 1, 1, 1, 0)] = 500000
        self.shape_score[(1, 1, 1, 1, 1)] = 50000000

    def upgrade(self, chess_board, x, y):
        self.board = chess_board
        self.current_x = x
        self.current_y = y
        self.current_color = chess_board.get_xy_color(x, y)
        self.list_2.append([x, y])
        self.list_3.append([x, y])
        self.list_all.remove([x, y])

    def calculate(self, is_ai):
        self.negamax(is_ai, self.depth, -99999999, 99999999, [None, None])
        #print('')
        #print(self.next_pt)
        self.list_1.append(self.next_pt)
        self.list_3.append(self.next_pt)
        self.list_all.remove(self.next_pt)
        return self.next_pt[0], self.next_pt[1]

    def evaluation(self, is_ai):
        if is_ai is True:
            my_list = self.list_1
            enemy_list = self.list_2
        else:
            my_list = self.list_2
            enemy_list = self.list_1

        my_score = 0
        for pt in my_list:
            m = pt[0]
            n = pt[1]
            my_score += self.cal_score(m, n, 0, 1, enemy_list, my_list)
            my_score += self.cal_score(m, n, 1, 0, enemy_list, my_list)
            my_score += self.cal_score(m, n, 1, 1, enemy_list, my_list)
            my_score += self.cal_score(m, n, -1, 1, enemy_list, my_list)

        enemy_score = 0
        for pt in enemy_list:
            m = pt[0]
            n = pt[1]
            enemy_score += self.cal_score(m, n, 0, 1, my_list, enemy_list)
            enemy_score += self.cal_score(m, n, 1, 0, my_list, enemy_list)
            enemy_score += self.cal_score(m, n, 1, 1, my_list, enemy_list)
            enemy_score += self.cal_score(m, n, -1, 1, my_list, enemy_list)

        total_score = my_score - enemy_score * self.ratio
        return total_score

    def cal_score(self, x, y, direc_x, direc_y, enemy_list, score_list):
        max_score = [0, [0, 0], [0, 0]]

        for i in range(-5, 1):
            color_list = []
            temp = []
            for j in range(0, 6):
                pt = [x + (i + j) * direc_x, y + (i + j) * direc_y]
                if pt[0] < 0 or pt[0] >= self.length or pt[1] < 0 or pt[1] >= self.length:
                    break
                if pt in enemy_list:
                    temp.append(2)
                elif pt in score_list:
                    temp.append(1)
                else:
                    temp.append(0)

            color_list.append(temp)
            color_list.append(temp[1:])
            color_list.append(temp[:-1])

            for item in color_list:
                if tuple(item) in self.shape_score.keys():
                    if self.shape_score[tuple(item)] >= max_score[0]:
                        max_score[0], max_score[1], max_score[2] = self.shape_score[tuple(item)], [x + i * direc_x, y + i * direc_y], [direc_x, direc_y]

        return max_score[0]

    def is_neiborhood(self, pt):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if [pt[0] + i, pt[1] + j] in self.list_3:
                    return True
        return False

    def order(self):
        self.search_begin_index_before.append(self.search_begin_index)
        for pt in self.list_3:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if [pt[0] + i, pt[1] + j] in self.list_all and self.list_all.index([pt[0] + i, pt[1] + j]) >= self.search_begin_index:
                        self.list_all.remove([pt[0] + i, pt[1] + j])
                        self.list_all.insert(0, [pt[0] + i, pt[1] + j])
                        self.search_begin_index += 1
        print(self.list_all)
        #print("last index: {}, current index: {}".format(self.search_begin_index_before[-1], self.search_begin_index))

    def negamax(self, is_ai, depth, alpha, beta, p):
        cut_flag = False
        if depth == 0 or ((depth != self.depth) and self.board.is_win(p[0], p[1])):
            return self.evaluation(is_ai)
        else:
            #print(depth, end=' ')
            self.order()
            for pt in self.list_all:
                if pt in self.list_3 or not self.is_neiborhood(pt):
                    continue
                """
                if depth == self.depth:
                    print(pt, end=' ')
                """
                if is_ai:
                    self.list_1.append(pt)
                    self.board.set_at_xy(pt[0], pt[1], 2)
                else:
                    self.list_2.append(pt)
                    self.board.set_at_xy(pt[0], pt[1], 1)
                self.list_3.append(pt)

                value = -self.negamax(not is_ai, depth - 1, -beta, -alpha, pt)

                if is_ai:
                    self.list_1.pop()
                else:
                    self.list_2.pop()
                self.board.set_at_xy(pt[0], pt[1], 0)
                self.list_3.pop()

                if value > alpha:
                    if depth == self.depth:
                        self.next_pt[0], self.next_pt[1] = pt[0], pt[1]
                    if value >= beta:
                        cut_flag = True
                        break
                    alpha = value

            num = self.search_begin_index - self.search_begin_index_before[-1]
            for i in range(num):
                self.list_all.insert(self.search_begin_index_before[-1], self.list_all.pop(0))
            self.search_begin_index = self.search_begin_index_before.pop()
            """
            if depth == self.depth:
                print('')
            """
            if cut_flag is True:
                return beta
            return alpha
