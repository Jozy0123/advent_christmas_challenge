from copy import deepcopy
class Rope:

    def __init__(self, starting_loc):

        if starting_loc is None:
            starting_loc = [0, 0]
        self.starting_loc = starting_loc

        self.ropes = [deepcopy(starting_loc) for _ in range(10)]

        self.tail_visited = set()
        self.tail_visited.add(tuple(i for i in self.ropes[-1]))

    def move(self, steps_count=0, direction='U'):

        if direction == 'U':
            multiplier = 1
            update_axis = 0
        elif direction == 'D':
            multiplier = -1
            update_axis = 0
        elif direction == 'L':
            multiplier = -1
            update_axis = 1
        elif direction == 'R':
            multiplier = 1
            update_axis = 1
        else:
            raise ValueError("this is for up and down")

        for _ in range(steps_count):

            self.ropes[0][update_axis] = self.ropes[0][update_axis] + 1 * multiplier

            for i in range(1, 10):
                relative_location = self.relative_location(i, i-1)
                if abs(relative_location[0]) < 2 and abs(relative_location[1]) < 2:
                    break
                else:
                    if abs(relative_location[0]) == 2 and abs(relative_location[1]) == 2:
                        self.ropes[i][0] = self.ropes[i-1][0] - int(relative_location[0]/2)
                        self.ropes[i][1] = self.ropes[i-1][1] - int(relative_location[1]/2)
                    elif abs(relative_location[0]) == 2:
                        self.ropes[i][0] = self.ropes[i-1][0] - int(relative_location[0]/2)
                        self.ropes[i][1] = self.ropes[i-1][1]
                    elif abs(relative_location[1]) == 2:
                        self.ropes[i][0] = self.ropes[i-1][0]
                        self.ropes[i][1] = self.ropes[i-1][1] - int(relative_location[1]/2)

            self.tail_visited.add(tuple(i for i in self.ropes[-1]))

    def relative_location(self, rope_loc_1, rope_loc_2):
        return [(self.ropes[rope_loc_2][i] - self.ropes[rope_loc_1][i]) for i in range(2)]

    def tailed_visited_loc(self):
        print(len(self.tail_visited))

    def is_diagonal(self, loc_1, loc_2):
        return [abs(self.ropes[loc_2][i] - self.ropes[loc_1][i]) for i in range(2)] == [1, 1]


def parse_line(line):
    line = line.rstrip()
    direction, steps = line.split(" ")[0], line.split(" ")[1]
    return direction, int(steps)

# def test_move():
#     rope = Rope()
#     rope.move(20, "U")
#     print(len(rope.tail_visited))
#     print(rope.head, rope.tail, rope.relative_location)

def calculate_visited():
    rope = Rope(starting_loc=[5, 11])
    with open("puzzle_input.txt", "r") as inputs:
        for line in inputs:
            direction, steps = parse_line(line)
            rope.move(steps, direction)
    rope.tailed_visited_loc()


if __name__ == "__main__":
    # test_move()
    calculate_visited()



