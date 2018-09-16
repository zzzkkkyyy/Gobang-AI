import sys

START = 1
END = 2
WALL = 3
ROAD = 0
DIST_RATIO = 10


class A_star(object):
    # construct maze
    row_count = 5
    col_count = 8
    map = {} # value: [type, G_value, H_value, father_pt=[]]
    start_pos = []
    end_pos = []

    # calculate needed
    open_list = []
    route_list = []

    def __init__(self):
        self.start_pos = [2, 1]
        self.end_pos = [2, 7]
        for i in range(self.row_count):
            for j in range(self.col_count):
                self.map[(i, j)] = [ROAD, 999999, 999999, None]
        for i in range(0, self.row_count - 1):
            self.map[(i, 3)][0] = WALL
        for i in range(1, self.row_count):
            self.map[(i, 5)][0] = WALL
        self.map[tuple(self.start_pos)][0] = START
        self.map[tuple(self.start_pos)][1] = 0
        self.map[tuple(self.start_pos)][2] = 0
        self.map[tuple(self.end_pos)][0] = END

    def manhattan_dist(self, pt, target_pt):
        return (abs(pt[0] - target_pt[0]) + abs(pt[1] - target_pt[1])) * DIST_RATIO

    def cal_g(self, current_pt, father_pt):
        if (current_pt[0] != father_pt[0]) and (current_pt[1] != father_pt[1]):
            g_value = self.map[tuple(father_pt)][1] + 14
        else:
            g_value = self.map[tuple(father_pt)][1] + 10
        return g_value

    def calculate_func(self, current_pt, father_pt):
        g_value = self.cal_g(current_pt, father_pt)
        h_value = self.manhattan_dist(current_pt, self.end_pos)
        self.map[tuple(current_pt)][1], self.map[tuple(current_pt)][2] = g_value, h_value

    def process(self):
        self.open_list.append(self.start_pos)
        while self.open_list is not None:
            min_f_value = 99999999
            min_pos = []
            for i in range(-1, 2):
                for j in range(-1, 2):
                    pt = [i + self.open_list[0][0], j + self.open_list[0][1]]
                    if pt[0] < 0 or pt[0] >= self.row_count or pt[1] < 0 or pt[1] >= self.col_count:
                        continue
                    if (i, j) == (0, 0) or self.map[tuple(pt)][0] == WALL or pt in self.route_list:
                        continue
                    elif pt in self.open_list:
                        if (self.map[tuple(self.open_list[0])][1] + self.cal_g(pt, self.open_list[0])) < self.map[tuple(pt)][1]:
                            self.map[tuple(pt)][1] = self.map[tuple(self.open_list[0])][1] + self.cal_g(pt, self.open_list[0])
                            self.map[tuple(pt)][3] = self.open_list[0]
                    else:
                        self.open_list.append(pt)
                        self.map[tuple(pt)][3] = self.open_list[0]
                        self.calculate_func(pt, self.open_list[0])
                        if pt == self.end_pos:
                            self.print_route(self.end_pos)
                            return
            for pt in self.open_list[1:]:
                if (self.map[tuple(pt)][1] + self.map[tuple(pt)][2]) <= min_f_value:
                    min_f_value = (self.map[tuple(pt)][1] + self.map[tuple(pt)][2])
                    min_pos = pt
            if min_pos == self.end_pos:
                self.print_route(self.end_pos)
                return
            self.route_list.append(self.open_list.pop(0))
            self.open_list.remove(min_pos)
            self.open_list.insert(0, min_pos)

    def print_route(self, pt=end_pos):
        if pt == self.start_pos:
            print(pt)
            return
        self.print_route(self.map[tuple(pt)][3])
        print('->')
        print(pt)


obj = A_star()
obj.process()
