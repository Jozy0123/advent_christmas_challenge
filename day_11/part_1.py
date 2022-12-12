from typing import List
from collections import deque


class Monkey:

    def __init__(self,
                 monkey_cnt: int,
                 starting_items: List[int],
                 stress_level_operation: str,
                 test_divisible_num: int,
                 results: List[int]):
        # results elements are corresponding to true and false.

        self.monkey_cnt = monkey_cnt
        self.items = []
        for i in starting_items:
            self.items.append(i)
        self.test_divisible_num = test_divisible_num
        self.results = results
        self.operation = Monkey.operation_helper(stress_level_operation)
        self.inspected = 0

    def start_play(self):
        throw_result = {}
        if len(self.items) < 1:
            return throw_result

        else:
            true_list = []
            false_list = []
            for i in self.items:
                new_item_level = self.operation(i)
                updated_value = round(new_item_level // 3)

                if updated_value % self.test_divisible_num == 0:
                    true_list.append(updated_value)
                else:
                    false_list.append(updated_value)
                self.inspected += 1

            self.items = []

            throw_result[self.results[0]] = true_list
            throw_result[self.results[1]] = false_list

            return throw_result

    def add_items(self, items):
        self.items += items

    @staticmethod
    def operation_helper(operation_string: str):

        def operation(operator: str, new_num: int):
            if operator == '*':
                return lambda x: x * (new_num if new_num != -1 else x)
            elif operator == '+':
                return lambda x: x + (new_num if new_num != -1 else x)

        operation_string = operation_string.rstrip()
        operation_string = operation_string.lstrip()
        num = operation_string.split(' ')[-1]
        operator = operation_string.split(' ')[-2]

        if num == 'old':
            new_num = -1
        else:
            new_num = int(num)

        return operation(operator, new_num)

    def print_items(self):
        print(f"Monkey {self.monkey_cnt}: {self.items}")


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
            i.print_items()

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
                    stress_level_operation=operation_string,
                    test_divisible_num=int(divisible),
                    results=[true_val, false_val]
                )
                play_round.add_monkey(monkey)
                continue

        monkey = Monkey(
            monkey_cnt=int(monkey_name),
            starting_items=starting_items,
            stress_level_operation=operation_string,
            test_divisible_num=int(divisible),
            results=[true_val, false_val]
        )
        play_round.add_monkey(monkey)

    return play_round


def simulation():
    play_round = parse_file()

    for _ in range(5):
        play_round.play()
        play_round.print_result()

    print(play_round.get_2_most_actives)


if __name__ == "__main__":
    simulation()
