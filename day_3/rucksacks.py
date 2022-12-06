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


def get_priority():
    priority_score = 0
    with open("rucksack.txt", "r") as rucksack:
        for line in rucksack:
            letters = set()
            line = line.rstrip()
            first_half = len(line) // 2
            for first_letter in line[:first_half]:
                letters.add(first_letter)
            for j in line[first_half:]:
                if j in letters:
                    priority_score += priority[j]
                    break
    return priority_score


if __name__ == "__main__":
    print(get_priority())
