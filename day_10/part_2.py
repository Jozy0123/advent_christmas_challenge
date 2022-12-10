class SPRITE:

    def __init__(self, register_value=1):
        self.register_value = register_value

    def update_location(self, update_value: int):
        self.register_value += update_value

    @property
    def pixels(self):
        return [self.register_value - 1, self.register_value, self.register_value + 1]


class CRTSCREEN:

    def __init__(self):
        self.screen = ''
        self.cycle = 0

    def lit_pixel(self, is_lit=False):
        if is_lit:
            self.screen += '#'
        else:
            self.screen += '.'

    def print_pixel(self):
        print(self.screen)

    def update_cycle(self, sprite):
        if (self.cycle % 40) in sprite.pixels:
            is_lit = True
        else:
            is_lit = False
        self.lit_pixel(is_lit)
        self.cycle += 1
        if self.cycle % 40 == 0:
            self.screen += '\n'


def print_crt_screen():

    crt_screen = CRTSCREEN()
    sprite = SPRITE()

    with open("puzzle_input.txt", "r") as inputs:
        for line in inputs:

            line_elem = line.rstrip().split(' ')
            if line_elem[0] == "noop":

                crt_screen.update_cycle(sprite)

            elif line_elem[0] == "addx":

                crt_screen.update_cycle(sprite)
                crt_screen.update_cycle(sprite)

                sprite.update_location(update_value=int(line_elem[1]))

    crt_screen.print_pixel()


if __name__ == "__main__":
    print_crt_screen()