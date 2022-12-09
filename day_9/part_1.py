class Rope:

    def __init__(self):

        self.starting_loc = [0, 0]
        self.head = [0, 0]
        self.tail = [0, 0]
        self.tail_visited = set()
        self.tail_visited.add(tuple(i for i in self.tail))

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

            self.head[update_axis] = self.head[update_axis] + 1 * multiplier
            relative_location = self.relative_location

            if abs(relative_location[0]) == 2:
                self.tail[0] = self.head[0] - int(relative_location[0]/2)
                self.tail[1] = self.head[1]
            elif abs(relative_location[1]) == 2:
                self.tail[0] = self.head[0]
                self.tail[1] = self.head[1] - int(relative_location[1]/2)

            self.tail_visited.add(tuple(i for i in self.tail))

    @property
    def relative_location(self):
        return [(self.head[i] - self.tail[i]) for i in range(2)]

    def tailed_visited_loc(self):
        print(len(self.tail_visited))

    @property
    def is_diagonal(self):
        return [abs(self.head[i] - self.tail[i]) for i in range(2)] == [1, 1]


def parse_line(line):
    line = line.rstrip()
    direction, steps = line.split(" ")[0], line.split(" ")[1]
    return direction, int(steps)


def test_move():
    rope = Rope()
    rope.move(20, "U")
    print(len(rope.tail_visited))
    print(rope.head, rope.tail, rope.relative_location)


def calculate_visited():
    rope = Rope()
    with open("puzzle_input.txt", "r") as inputs:
        for line in inputs:
            direction, steps = parse_line(line)
            rope.move(steps, direction)
    rope.tailed_visited_loc()


if __name__ == "__main__":
    # test_move()
    calculate_visited()



