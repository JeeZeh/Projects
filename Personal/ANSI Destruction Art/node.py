import colours as c
import random

dissolve_chars = {
    "text": {
        3: ["∄", "∉", "∎", "Д", "⍬", "≨", "#"],
        2: ["∺", "∾", ";", "∢", "⊹", "≄", "π"],
        1: ["`", "¬", "∵", "᛫", "⋅", "⋄", "^"],
    },
    "block": {3: ["▓"], 2: ["▒"], 1: ["░"]},
}

class Node:
    """
    Node containing a string, health and colour
    """

    MAX_HEALTH = 4
    version = "text"
    source = ""
    health = 0
    state = []
    healthy = True
    colour = c.ENDC
    theme = [c.ENDC, c.OKBLUE, c.WARNING, c.FAIL]
    dead = False

    def __init__(self, source, colour=c.ENDC, health=MAX_HEALTH, version="text", theme=theme):
        self.source = source
        self.colour = colour
        if len(theme) != self.MAX_HEALTH:
            raise ValueError(f"Colour list {theme} does not match MAX_HEALTH ({self.MAX_HEALTH})")
        self.theme = theme
        self.health = len(source) * self.MAX_HEALTH
        self.state = [(s, self.MAX_HEALTH) for s in source]
        self.version = version
        if health != self.MAX_HEALTH:
            self.update_state()

    def set_source(self, source):
        self.source = source

    def set_colour(self, colour):
        self.colour = colour

    def set_health(self, health):
        self.state = [(c[0], health) for c in self.state]
        self.update_state()

    def reset(self):
        self.health = self.MAX_HEALTH
        self.state = self.source
        self.colour = c.ENDC

    def update_state(self):
        """
        Updates the node characters based on health.
        """

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
                    self.state[i] = (random.choice(dissolve_chars[self.version][h]), h)
            else:
                dead = False
        self.dead = dead

    def attack(self, times=1):
        """
        Decrement the health
        """
        if not self.dead:
            for _ in range(times):
                self.health -= 1
                remaining = [x for x, char in enumerate(self.state) if char[1] > 0]
                attack = remaining[random.randint(0, len(remaining) - 1)]
                self.state[attack] = (self.state[attack][0], self.state[attack][1] - 1)
            self.update_state()

    def __repr__(self):
        return "".join(
            map(lambda x: f"{self.theme[max(0, x[1]-1)]}{x[0]}{c.ENDC}", self.state)
        )

    def __str__(self):
        return "".join(
            map(lambda x: f"{self.theme[max(0, x[1]-1)]}{x[0]}{c.ENDC}", self.state)
        )
