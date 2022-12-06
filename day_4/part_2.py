def parse_range(line):
    pairs = []
    for section in line.rstrip().split(","):
        for num in section.split("-"):
            pairs.append(int(num))
    if pairs[0] > pairs[2]:
        pairs[0], pairs[1], pairs[2], pairs[3] = pairs[2], pairs[3], pairs[0], pairs[1]
    return pairs[1] >= pairs[2]


def test_parse_range():
    line = "51-96,55-99\n"
    print(parse_range(line))


def calculate_assignment_containment():
    final_score = 0
    with open("puzzle_input.txt", "r") as lines:
        for line in lines:
            score = parse_range(line)
            print(score)
            final_score += score
    return final_score


if __name__ == "__main__":
    test_parse_range()
    print(calculate_assignment_containment())
