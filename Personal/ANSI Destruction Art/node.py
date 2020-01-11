import colours as c
from random import randint

health_map = {
    3: ["∄", "∉", "∎", "∂", "Z", "≨", "#"],
    2: ["∺", "∾", " ", "∢", "⊹", "≄", " "],
    1: [" ", " ", "∵", " ", "⋅", "⋄", " "],
}


class Node:
    """
    Node containing a string, health and colour
    """

    string = ""
    health = 4
    broken = ""
    colour = ""

    def __init__(self, string, colour=None, health=None):
        self.string = string
        if colour is not None:
            self.colour = colour
        if health is not None:
            self.health = health

    def set_string(self, string):
        self.string = string

    def set_colour(self, colour):
        self.colour = colour

    def set_health(self, health):
        self.health = health
        self.gen_broken()

    def gen_broken(self):
        """
        Generates a new broken version of the node based on health
        """

        if 0 < self.health < 4:
            self.broken = "".join(
                [
                    health_map[self.health][randint(0, 6)]
                    if randint(0, 3) > self.health - 1
                    else char
                    for char in self.string
                ]
            )
        elif self.health <= 0:
            self.broken = " " * len(self.string)

    def hurt(self):
        """
        Decrement the health
        """
        if self.health > 0:
            self.health -= 1
            self.gen_broken()

    def get_string(self):
        return self.string

    def get_colour(self):
        return self.colour

    def get_health(self):
        return self.health

    def __repr__(self):
        return f"{self.colour}{self.string if self.health == 4 else self.broken}{c.ENDC}"

    def __str__(self):
        return f"{self.colour}{self.string if self.health == 4 else self.broken}{c.ENDC}"
