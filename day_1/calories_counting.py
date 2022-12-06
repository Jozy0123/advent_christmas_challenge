def most_calories():

    current_calories = 0
    max_calories = 0
    with open("calories.txt", "r") as calories:
        for line in calories:
            if line != "" and line != "\n":
                current_calories += int(line)
            else:
                if current_calories >= max_calories:
                    max_calories = current_calories
                current_calories = 0
    return max_calories


def top_3_calories():

    top_3 = [0, 0, 0]
    current_calories = 0
    with open("calories.txt", "r") as calories:
        for line in calories:
            if line != "" and line != "\n":
                current_calories += int(line)
            else:
                top_3.append(current_calories)
                top_3 = sorted(top_3, reverse=True)[:3]
                current_calories = 0
    return sum(top_3)


if __name__ == "__main__":
    print(most_calories())
    print(top_3_calories())
