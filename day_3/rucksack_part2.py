import string

lower_case_letters = string.ascii_lowercase
upper_case_letters = string.ascii_uppercase

priority = {}

i = 0
for letter in lower_case_letters:
    i += 1
    priority[letter] = i

for letter in upper_case_letters:
    i += 1
    priority[letter] = i


def find_common_letter(line1, line2, line3):
    letters = set()
    for letter in line1.rstrip():
        letters.add(letter)

    new_letters = set()
    for letter in line2.rstrip():
        if letter in letters:
            new_letters.add(letter)

    for letter in line3.rstrip():
        if letter in new_letters:
            return priority[letter]


def get_priority_score():
    total_score = 0
    with open("rucksack.txt", "r") as rucksack:
        groups = []
        i = 0
        for line in rucksack:
            groups.append(line)
            i += 1
            if i % 3 == 0:
                total_score += find_common_letter(*groups)
                i = 0
                groups = []
                continue
    return total_score


if __name__ == "__main__":
    print(get_priority_score())
