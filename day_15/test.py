from functools import reduce
from typing import Tuple, List
from itertools import product

def manhattan_distance(loc1: Tuple[int, int],
                       loc2: Tuple[int, int]) -> int:
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])


def all_locs_same_manhattan_distance(loc: Tuple[int, int],
                                     dist: int) -> List[Tuple[int, int]]:

    x_axis_range = range(loc[0] - dist, loc[0] + dist + 1, 1)
    y_axis_range = range(loc[1] - dist, loc[1] + dist + 1, 1)

    all_locs = [(i, j) for i, j in product(x_axis_range, y_axis_range) if manhattan_distance((i, j), loc) <= dist]

    return all_locs


class Sensor:

    def __init__(self, loc, beacon):
        self.loc = loc
        self.beacon = beacon

    @property
    def manhattan_distance_1(self):
        return manhattan_distance(self.loc, self.beacon)

    def check_rows_max_dist(self, y):
        dist_to_row = manhattan_distance(self.loc, (self.loc[0], y))
        if self.manhattan_distance_1 < dist_to_row:
            return None
        else:
            return ((self.loc[0] - (self.manhattan_distance_1 - dist_to_row))
                    , (self.loc[0] + (self.manhattan_distance_1 - dist_to_row)))
    def rotate_45(self):
        return self.loc[0] + self.loc[1], self.loc[1] - self.loc[0]

    def get_locs(self):
        return all_locs_same_manhattan_distance(self.loc, self.manhattan_distance_1)




def test_locs(sensors):
    lists = set()
    for sensor in sensors:
        for loc in sensor.get_locs():
            lists.add(loc)

    for i in range(0, 20, 1):
        for j in range(0, 20, 1):
            if (i, j) in lists:
                print("#", end='')
            else:
                print(".", end='')
        print("\n")

    # print(parse_line("Sensor at x=2, y=18: closest beacon is at x=-2, y=15\n"))

def parse_line(line):
    line = line.rstrip()
    sensor = line.split(": ")[0]
    beacon = line.split(": ")[1]

    sensor_x = sensor.split(", ")[0].split(" ")[-1].split("=")[1]
    sensor_y = sensor.split(", ")[1].split(" ")[-1].split("=")[1]

    beacon_x = beacon.split(", ")[0].split(" ")[-1].split("=")[1]
    beacon_y = beacon.split(", ")[1].split(" ")[-1].split("=")[1]

    return (int(sensor_x), int(sensor_y)), (int(beacon_x), int(beacon_y))


def parse_input():
    sensor_lists = []
    beacon_lists = []
    with open("puzzle_input.txt", "r") as inputs:
        for line in inputs:
            sensor, beacon = parse_line(line)
            sensor_lists.append(sensor)
            beacon_lists.append(beacon)

    return sensor_lists, beacon_lists

def merge_lists(lst):
    results = []
    def determine_range(x, y):
        if x[1] >= y[0] and y[1] >= x[1]:
            return x[0], y[1]
        elif x[1] >= y[0] and y[1] < x[1]:
            return x[0], x[1]
        elif x[1] < y[0]:
            return [x, y]

    for i in range(len(lst)-1):
        result = determine_range(lst[i], lst[i+1])
        if isinstance(result, tuple):
            results.append(result)
        else:
            for j in result:
                results.append(j)

    return results


def calculate(row):
    shined_through = []
    rotated = []
    sensors = parse_input()
    beacon_ys = set()
    for i, j in zip(sensors[0], sensors[1]):
        print("================================")
        sensor = Sensor(loc=i, beacon=j)
        rotated.append(sensor.rotate_45())
        shined_through.append(sensor)
        test_locs(shined_through)
        print("================================")

    rotated.sort()
    print(rotated)
    #
    # shined_through.sort()
    #
    # num_set = set()
    # for i in shined_through:
    #     for j in range(i[0], i[1]+1):
    #         if j not in num_set and (j, row) not in beacon_ys:
    #             num_set.add(j)
    # return len(num_set)


if __name__ == "__main__":
    # test_locs()
    print(calculate(2000000))