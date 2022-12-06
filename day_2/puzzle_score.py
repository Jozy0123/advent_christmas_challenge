from dataclasses import dataclass
from enum import Enum
from typing import Literal


class Scores(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3


class RockPaperScissors:

    def __init__(self, value):
        if value in {"A", "X"}:
            self.shape = Scores.Rock
        elif value in {"B", "Y"}:
            self.shape = Scores.Paper
        elif value in {"C", "Z"}:
            self.shape = Scores.Scissors

    def __eq__(self, other):
        return self.shape.name == other.shape.name

    def __gt__(self, other):
        if self.shape.name == "Rock" and other.shape.name == "Scissors":
            return True
        elif self.shape.name == "Scissors" and other.shape.name == "Paper":
            return True
        elif self.shape.name == "Paper" and other.shape.name == "Rock":
            return True
        else:
            return False


def score_cal(opponent_shape: RockPaperScissors,
              your_shape: RockPaperScissors):
    score = your_shape.shape.value

    if opponent_shape == your_shape:
        score += 3
    elif opponent_shape < your_shape:
        score += 6

    return score


def total_score():
    score = 0
    with open("puzzle_input.txt", "r") as input:
        for line in input:
            pair = line.rstrip().split(" ")
            score += score_cal(RockPaperScissors(pair[0]), RockPaperScissors(pair[1]))
    return score


if __name__ == "__main__":

    print(total_score())
