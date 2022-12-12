from typing import List, Tuple
from collections import deque


class MonkeyNum:
    def __init__(self, starting_num):
        self.starting_num = starting_num
        self.divisible_tests = {}

    def update(self, operator, new_num):

        if new_num == 'old':
            for key, value in self.divisible_tests.items():
                self.divisible_tests[key] = (value ** 2) % key

        if new_num != 'old':
            new_num = int(new_num)
            if operator == '+':
                for key, value in self.divisible_tests.items():
                    self.divisible_tests[key] = (value + new_num) % key

            elif operator == '*':
                for key, value in self.divisible_tests.items():
                    self.divisible_tests[key] = (value % key) * (new_num % key)

    def divisible(self, num):
        if self.divisible_tests.get(num) == 0:
            return True
        else:
            return False

    def init_divisible_tests(self, divisible_tests_lists):
        for i in divisible_tests_lists:
            self.divisible_tests[i] = self.starting_num % i

class Monkey:

    def __init__(self,
                 monkey_cnt: int,
                 starting_items: List[int],
                 operation_string: str,
                 test_divisible_num: int,
                 results: List[int]):
        # results elements are corresponding to true and false.

        self.monkey_cnt = monkey_cnt
        self.items = []
        for i in starting_items:
            monkey_num = MonkeyNum(i)
            self.items.append(monkey_num)
        self.test_divisible_num = test_divisible_num
        self.results = results
        self.inspected = 0
        self.operator, self.operator_num = self.operation_helper(operation_string)

    def start_play(self):
        throw_result = {}
        if len(self.items) < 1:
            return throw_result

        else:
            true_list = []
            false_list = []
            for i in self.items:
                i.update(self.operator, self.operator_num)
                if i.divisible(self.test_divisible_num):
                    true_list.append(i)
                else:
                    false_list.append(i)
                self.inspected += 1

            self.items = []

            throw_result[self.results[0]] = true_list
            throw_result[self.results[1]] = false_list

            return throw_result

    def add_items(self, items):
        self.items += items

    @staticmethod
    def operation_helper(operation_string):

        operation_string = operation_string.rstrip()
        operation_string = operation_string.lstrip()
        num = operation_string.split(' ')[-1]
        operator = operation_string.split(' ')[-2]

        return operator, num

    def print_inspected(self):
        print(f"Monkey {self.monkey_cnt} inspected: {self.inspected}")


class Round:

    def __init__(self):
        self.round = 0
        self.monkey_list = []

    def add_monkey(self, monkey: Monkey):
        self.monkey_list.append(monkey)

    def play(self):
        for i in self.monkey_list:
            throw_result = i.start_play()

            for key, value in throw_result.items():
                if value is not None and value != []:
                    self.monkey_list[key].add_items(value)
        self.round += 1

    def print_result(self):
        print(f"round is {self.round}")
        for i in self.monkey_list:
            i.print_inspected()

    @property
    def get_2_most_actives(self):
        lst = []
        for i in self.monkey_list:
            lst.append(i.inspected)
        lst.sort(reverse=True)

        return lst[0] * lst[1]


def parse_file():
    play_round = Round()

    with open("puzzle_input.txt", "r") as puzzle_input:
        for line in puzzle_input:
            line = line.rstrip().lstrip()
            if line.startswith("Monkey"):
                monkey_name = line[:-1].split(" ")[-1]
            elif line.startswith("Starting"):
                starting_items = [int(i) for i in line.split(':')[-1].split(",")[:]]
            elif line.startswith("Operation"):
                operation_string = line
            elif line.startswith("Test"):
                divisible = line.split(" ")[-1]
            elif line.startswith("If true"):
                true_val = int(line.split(" ")[-1])
            elif line.startswith("If false"):
                false_val = int(line.split(" ")[-1])
            else:
                monkey = Monkey(
                    monkey_cnt=int(monkey_name),
                    starting_items=starting_items,
                    operation_string=operation_string,
                    test_divisible_num=int(divisible),
                    results=[true_val, false_val]
                )
                play_round.add_monkey(monkey)
                continue

        monkey = Monkey(
            monkey_cnt=int(monkey_name),
            starting_items=starting_items,
            operation_string=operation_string,
            test_divisible_num=int(divisible),
            results=[true_val, false_val]
        )
        play_round.add_monkey(monkey)

    return play_round


def simulation():
    play_round = parse_file()
    divisible_list = []
    for monkey in play_round.monkey_list:
        divisible_list.append(monkey.test_divisible_num)

    for monkey in play_round.monkey_list:
        for i in monkey.items:
            i.init_divisible_tests(divisible_list)

    for _ in range(10000):
        play_round.play()

    play_round.print_result()
    print(play_round.get_2_most_actives)


if __name__ == "__main__":
    simulation()
