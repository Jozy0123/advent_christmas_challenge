from dataclasses import dataclass
from enum import Enum
from typing import Literal


class Scores(Enum):
    A = 1
    B = 2
    C = 3


class Results(Enum):
    X = 0
    Y = 3
    Z = 6


winning_pairs = {
    "A": "C",
    "C": "B",
    "B": "A"
}


class RockPaperScissors:

    def __init__(self, value):
        self.shape = Scores[value]
        self.value = value

    def get_correct_shape_score(self, result) -> int:

        winning_shape = winning_pairs[self.value]
        winning_value = Scores[winning_shape].value

        result = Results[result]
        if result.value == 3:
            return Scores[self.value].value
        elif result.value == 6:
            return list({1, 2, 3} - {self.shape.value, winning_value})[0]
        else:
            return winning_value


def score_cal(opponent_shape: RockPaperScissors, letters):
    score = Results[letters].value
    score += opponent_shape.get_correct_shape_score(letters)
    return score


def total_score():
    score = 0
    with open("puzzle_input.txt", "r") as input:
        for line in input:
            pair = line.rstrip().split(" ")
            score += score_cal(RockPaperScissors(pair[0]), pair[1])
    return score


if __name__ == "__main__":
    print(total_score())
