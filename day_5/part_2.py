class ModifiedStack:

    def __init__(self, list_of_object=None):
        if list_of_object is None:
            list_of_object = []
        self.list_of_object = list_of_object

    def pop(self, num_of_elems):
        last = self.list_of_object[-num_of_elems:]
        self.list_of_object = self.list_of_object[:-num_of_elems]
        return last

    def push(self, values):
        self.list_of_object += values

    def peek(self):
        return self.list_of_object[-1]

    def __repr__(self):
        return f"[{','.join(self.list_of_object)}]"


def parse_stacks(line):
    objects = []
    length = len(line)
    pointer = 1
    while pointer < length:
        if line[pointer] == ' ' or line[pointer] == '':
            objects.append(None)
        else:
            objects.append(line[pointer])
        pointer += 4
    return objects


def parse_input(filename):
    stacks = []
    moving_steps = []
    with open(filename, 'r') as inputs:
        for line in inputs:
            if line != '' and line != '\n':
                stacks.append(line)
            else:
                break

        for line in inputs:
            moving_steps.append([int(i) for i in line.rstrip().split(' ')[1::2]])

    stacks.reverse()
    num_of_stacks = int(stacks[0].rstrip()[-1])
    return stacks[1:], moving_steps, num_of_stacks


def test_parse_stacks():
    line = "[W]     [J] [L]             [J] [V]\n"
    print(parse_stacks(line))


def calculate_stop_stack():
    final_string = ''
    stack_list = []

    stacks, moving_steps, num_of_stacks = parse_input("puzzle_input.txt")
    for _ in range(num_of_stacks):
        stack_list.append(ModifiedStack())

    for stack in stacks:
        objects = parse_stacks(stack)
        for i in range(len(objects)):
            if objects[i] is not None:
                stack_list[i].push(objects[i])

    for step in moving_steps:
        num_moving = step[0]
        starting = step[1]
        ending = step[2]

        elem = stack_list[starting-1].pop(num_moving)
        stack_list[ending-1].push(elem)

    for i in stack_list:
        final_string += i.peek()

    return final_string


if __name__ == '__main__':
    test_parse_stacks()
    print(calculate_stop_stack())
