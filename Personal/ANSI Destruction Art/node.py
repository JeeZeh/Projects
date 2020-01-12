import colours as c
from random import randint

health_map = {
    3: ["∄", "∉", "∎", "Д", "⍬", "≨", "#"],
    2: ["∺", "∾", ";", "∢", "⊹", "≄", "π"],
    1: ["`", "¬", "∵", "᛫", "⋅", "⋄", "^"],
}

colours = [c.ENDC, c.OKBLUE, c.WARNING, c.FAIL]
colours.reverse()


class Node:
    """
    Node containing a string, health and colour
    """

    MAX_HEALTH = 4
    source = ""
    health = MAX_HEALTH
    state = ""
    healthy = True
    colour = c.ENDC
    dead = False

    def __init__(self, source, colour=c.ENDC, health=MAX_HEALTH):
        self.source = source
        self.colour = colour
        self.health = health
        self.state = [(s, self.MAX_HEALTH) for s in source]
        if health != self.MAX_HEALTH:
            self.update_state()

    def set_source(self, source):
        self.source = source

    def set_colour(self, colour):
        self.colour = colour

    def set_health(self, health):
        self.state = [(c[0], health) for c in self.state]
        self.update_stateV2()

    def reset(self):
        self.health = self.MAX_HEALTH
        self.state = self.source
        self.colour = c.ENDC

    def update_state(self):
        """
        Generates a new state of the node based on health
        """

        if 0 < self.health < 4:
            self.healthy = False
            self.state = "".join(
                [
                    health_map[self.health][randint(0, 6)]
                    if randint(0, 3) > self.health - 1
                    else char
                    for char in self.source
                ]
            )
        elif self.health <= 0:
            self.dead = True
            self.state = " " * len(self.source)

    def update_stateV2(self):
        dead = True
        remaining = [x for x, char in enumerate(self.state) if char[1] >= 0]
        for i in remaining:
            h = self.state[i][1]
            if h < 4:
                if h <= 0:
                    self.state[i] = (" ", h - 1)
                else:
                    dead = False
                    self.healthy = False
                    self.state[i] = (health_map[h][randint(0, 5)], h)
            else:
                dead = False
        self.dead = dead

    def hurt(self):
        """
        Decrement the health
        """
        if not self.dead:
            remaining = [x for x, char in enumerate(self.state) if char[1] > 0]
            attack = remaining[randint(0, len(remaining) - 1)]
            self.state[attack] = (self.state[attack][0], self.state[attack][1] - 1)
            self.update_stateV2()

    def __repr__(self):
        return "".join(
            map(lambda x: f"{colours[max(0, x[1]-1)]}{x[0]}{c.ENDC}", self.state)
        )

    def __str__(self):
        return "".join(
            map(lambda x: f"{colours[max(0, x[1]-1)]}{x[0]}{c.ENDC}", self.state)
        )
