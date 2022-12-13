from collections import deque
from string import ascii_lowercase

letter_order = {v: k for k, v in enumerate(ascii_lowercase)}


class HeightMap:

    def __init__(self, map_list):
        self.maps = map_list
        self.boundary = (len(self.maps), len(self.maps[1]))
        self.records = deque()
        self.visited = set()

    def passable(self, loc, current_loc):

        return letter_order[self.maps[loc[0]][loc[1]]] - letter_order[self.maps[current_loc[0]][current_loc[1]]] <= 1

    def check_if_legit_loc(self, i):
        if i[0] < 0 or i[1] < 0 or i[0] > (self.boundary[0] - 1) or i[1] > (self.boundary[1] - 1):
            return False
        else:
            return True

    def check_surrounding(self, current_loc):

        class Player:

            def __init__(self, loc):
                self.loc = loc

        player = Player(current_loc)

        surroundings = []

        tuple_pairs = ((player.loc[0] - 1, player.loc[1]),
                       (player.loc[0] + 1, player.loc[1]),
                       (player.loc[0], player.loc[1] - 1),
                       (player.loc[0], player.loc[1] + 1))

        for i in tuple_pairs:
            is_valid = self.check_if_legit_loc(i)
            if not is_valid or i in self.visited:
                continue
            else:
                if self.passable(i, current_loc):
                    surroundings.append(i)

        if not surroundings:
            return None
        else:
            return surroundings

    def play(self, init_loc, signal_loc):

        keep_path = {}

        self.records.append(init_loc)
        self.visited.add(init_loc)

        while not len(self.records) == 0:
            loc = self.records.pop()
            if loc == signal_loc:
                return keep_path
            current_loc = loc
            surroundings = self.check_surrounding(current_loc)
            if surroundings is None:
                continue
            for i in surroundings:
                self.records.appendleft(i)
                keep_path[i] = current_loc
                self.visited.add(i)

        return keep_path


def parse_file():
    with open("puzzle_input.txt", 'r') as inputs:
        map_list = []
        row_cnt = 0
        init_locs = []
        for line in inputs:
            col_cnt = 0
            row = []
            for i in line.rstrip():
                if i == 'S' or i == 'a':
                    init_locs.append((row_cnt, col_cnt))
                    i = 'a'
                elif i == 'E':
                    end_loc = (row_cnt, col_cnt)
                    i = 'z'
                row.append(i)
                col_cnt += 1
            map_list.append(row)
            row_cnt += 1

    return map_list, init_locs, end_loc


if __name__ == '__main__':
    map_list, init_locs, end_loc = parse_file()
    print(init_locs, end_loc)

    smallest_path = 0

    for init_loc in init_locs:
        map = HeightMap(map_list)
        keep_path = map.play(init_loc, end_loc)
        i = end_loc
        path = []
        while True:
            if keep_path.get(i) is None:
                break
            else:
                path.append(keep_path[i])
                i = keep_path[i]

        paths_len = len(path)

        print(paths_len)

        if paths_len != 0 and smallest_path == 0:
            smallest_path = paths_len
        elif paths_len == 0:
            continue
        elif paths_len < smallest_path:
            smallest_path = paths_len

    print(smallest_path)