def update_register_value() -> int:

    cycle_stopping_interval = set(range(20, 230, 40))
    cycle = 0
    register_value = 1
    signal_strength = 0

    with open("puzzle_input.txt", "r") as inputs:
        for line in inputs:

            line_elem = line.rstrip().split(' ')
            if line_elem[0] == "noop":

                cycle += 1
                if cycle in cycle_stopping_interval:
                    signal_strength += cycle * register_value

            elif line_elem[0] == "addx":

                cycle += 1
                if cycle in cycle_stopping_interval:
                    signal_strength += cycle * register_value

                cycle += 1
                if cycle in cycle_stopping_interval:
                    signal_strength += cycle * register_value

                register_value += int(line_elem[1])

    return signal_strength


if __name__ == "__main__":
    print(update_register_value())

