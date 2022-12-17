from functools import reduce
from typing import Tuple, List
from itertools import product, combinations
from collections import deque


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
        self.manhattan_distance = manhattan_distance(self.loc, self.beacon)

    def check_rows_max_dist(self, y):
        dist_to_row = manhattan_distance(self.loc, (self.loc[0], y))
        if self.manhattan_distance < dist_to_row:
            return None
        else:
            return ((self.loc[0] - (self.manhattan_distance - dist_to_row))
                    , (self.loc[0] + (self.manhattan_distance - dist_to_row)))

    @property
    def get_4_points(self):
        return (self.loc[0], self.loc[1] + self.manhattan_distance), \
            (self.loc[0], self.loc[1] - self.manhattan_distance), \
            (self.loc[0] + self.manhattan_distance, self.loc[1]), \
            (self.loc[0] + self.manhattan_distance, self.loc[1])

    def get_range(self, row):
        # print(row, self.loc)
        # print(abs(row - self.loc[1]), self.manhattan_distance)
        dist = abs(row - self.loc[1])
        if dist <= self.manhattan_distance:

            starting = self.manhattan_distance - dist

            return self.loc[0] - starting, self.loc[0] + starting


    def if_contain_point(self, point):
        return manhattan_distance(self.loc, point) <= self.manhattan_distance

    def check_if_1_more(self, point):
        if manhattan_distance(self.loc, point) - self.manhattan_distance == 1:
            return True
        else:
            return False

class Line:

    def __init__(self, ratio, intercept):
        self.intercept = intercept
        self.ratio = ratio

    def interceptions(self, another):
        if self.ratio == another.ratio:
            return None
        else:
            y = (self.intercept + another.intercept) / 2
            x = y + self.intercept
            return (x, y)


def test_locs():
    sensor = (8, 7)
    dist = 9
    get_list = all_locs_same_manhattan_distance(sensor, dist)
    for i in range(-1, 25, 1):
        for j in range(-2, 22, 1):
            if (i, j) in get_list:
                print("#", end='')
            else:
                print(".", end='')
        print("\n")

    print(parse_line("Sensor at x=2, y=18: closest beacon is at x=-2, y=15\n"))


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
    final_lsts = []

    def determine_range(x, y):
        if x[1] >= y[0] and y[1] >= x[1]:
            return x[0], y[1]
        elif x[1] >= y[0] and y[1] <= x[1]:
            return x[0], x[1]
        return None

    results = deque()
    for i in lst:
        results.appendleft(i)
    # print(results)

    while not len(results) <= 1:

        first_elem = results.pop()
        second_elem = results.pop()
        elem = determine_range(first_elem, second_elem)
        # print(first_elem, second_elem, elem)
        if elem is None:
            final_lsts.append(first_elem)
            results.append(second_elem)
        else:
            results.append(elem)

    final_lsts.append(results.pop())

    return final_lsts


def calculate_test(sensors, row):
    sensor_lists = []
    for i, j in zip(sensors[0], sensors[1]):
        sensor = Sensor(loc=i, beacon=j)
        sensor_lists.append(sensor)

    for i in range(row, -1, -1):
        shined_through = [sensor.check_rows_max_dist(i) for sensor in sensor_lists]
        shined_through = [i for i in shined_through if i is not None]
        shined_through.sort(key = lambda x:x[0])
        # print(shined_through)
        merged = merge_lists(shined_through)
        print(i, merged)

        if len(merged) > 1:
            print((merged[0][1] + 1) * 4000000 + i)
            return merged



def calculate(sensors, row):
    sensors_lists = []
    # finals = set()
    # points = set()
    for i, j in zip(sensors[0], sensors[1]):
        sensor = Sensor(loc=i, beacon=j)
        print(sensor.get_4_points)
        sensors_lists.append(sensor)


def find_signal(row):
    sensors = parse_input()
    calculate_test(sensors, row)


if __name__ == "__main__":
    # test_locs()
    # print(calculate(9))
    find_signal(4000000)
