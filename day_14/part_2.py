from typing import List, Tuple


def tuple_pair_process(t1, t2):
    lsts = []
    if t1[0] == t2[0]:
        if t1[1] < t2[1]:
            for i in range(t1[1], t2[1] + 1):
                lsts.append((t1[0], i))
        elif t1[1] > t2[1]:
            for i in range(t2[1], t1[1] + 1):
                lsts.append((t1[0], i))
    elif t1[1] == t2[1]:
        if t1[0] < t2[0]:
            for i in range(t1[0], t2[0] + 1):
                lsts.append((i, t1[1]))
        elif t1[0] > t2[0]:
            for i in range(t2[0], t1[0] + 1):
                lsts.append((i, t1[1]))
    return lsts


def generate_expanded_lists(location_range: List[Tuple[int, int]]):
    explanded_lists = []

    for i in range(len(location_range) - 1):
        explanded_lists += tuple_pair_process(location_range[i], location_range[i + 1])
        i += 1

    return explanded_lists


def parse_line(line):
    line = line.rstrip()
    tuples = line.split(' -> ')
    lsts = []
    for i in tuples:
        lsts.append([int(j) for j in i.split(',')])

    return lsts


def parse_file():
    final_lists = set()
    with open("puzzle_input.txt", "r") as inputs:
        for line in inputs:
            lsts = parse_line(line)
            for i in generate_expanded_lists(lsts):
                final_lists.add(i)
    return final_lists


class Space:

    def __init__(self, blocked_loc):
        if blocked_loc is None:
            blocked_loc = set()
        self.blocked_loc = blocked_loc
        self.max_height = max(self.blocked_loc, key=lambda x: x[1])[1] + 2

    def move_sand(self):

        while True:
            sand = Sand()
            while True:

                if sand.loc[1] + 1 != self.max_height:
                    if (sand.loc[0], sand.loc[1] + 1) not in self.blocked_loc:
                        sand.loc = (sand.loc[0], sand.loc[1] + 1)
                    elif (sand.loc[0] - 1, sand.loc[1] + 1) not in self.blocked_loc:
                        sand.loc = (sand.loc[0] - 1, sand.loc[1] + 1)
                    elif (sand.loc[0] + 1, sand.loc[1] + 1) not in self.blocked_loc:
                        sand.loc = (sand.loc[0] + 1, sand.loc[1] + 1)
                    else:
                        break
                else:
                    break

            self.blocked_loc.add(sand.loc)
            if sand.loc[1] == 0:
                break

        return Sand.get_sand_num()

class Sand:
    sand_num = 0

    def __init__(self, init_loc=(500, 0)):
        self.loc = init_loc
        Sand.sand_num += 1

    @classmethod
    def get_sand_num(cls):
        return Sand.sand_num


if __name__ == '__main__':
    result = parse_file()
    space = Space(result)
    print(space.move_sand())

