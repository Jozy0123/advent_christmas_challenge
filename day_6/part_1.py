def get_marker_position():

    with open("puzzle_input.txt", "r") as puzzle:
        for line in puzzle:
            for i in range(4, len(line)):
                tuple_of_elem = {j for j in line[i-4:i]}
                if len(tuple_of_elem) == 4:
                    return i
                else:
                    continue


if __name__ == "__main__":
    print(get_marker_position())

