from node import Node
import colours as c
from time import sleep
from itertools import permutations
import os
import random as r

SEP = f"{c.ENDC} "

THEME_STD = [c.FAIL, c.WARNING, c.OKBLUE, c.ENDC]
THEME_MONO = [c.ENDC] * 4
THEME_LOW_HEALTH = [c.FAIL, c.ENDC, c.ENDC, c.ENDC]


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def demo():
    """
    Shows destruction type at each health level
    """

    text = input()
    if not text:
        text = "This is a demo\ntesting text destruction\nusing ANSI colours\nin a random but progressive style!".splitlines()
    else:
        text = text.split("  ")
    colours = [c.UNDERLINE, c.OKBLUE, c.WARNING, c.FAIL]
    while True:
        for _ in range(FRAMERATE):
            rows = []
            for i in range(0, 4):
                rows.append([Node(t, colour=c.UNDERLINE) for t in text])
                for n in rows[-1]:
                    n.set_health(4 - i)
                    n.set_colour(colours[i])
            output = "\n".join([SEP.join(map(repr, row)) for row in rows])
            cls()
            print(output)
            sleep(1 / FRAMERATE)


def generate_column(template=None, random=True, width=8, height=20, theme=THEME_STD):
    if template and random:
        template = list(map(str, template))
        column = []
        for _ in range(height):
            r.shuffle(template)
            column.append(Node("".join(template), theme=theme))
    elif template and not random:
        template = list(map(str, template))
        column = [Node(template, theme=theme) for _ in range(height)]
    else:
        column = [
            Node("█" * width, version="block", theme=theme) for _ in range(height)
        ]

    return column


class BreakIt(Exception):
    pass


def dissolve(collection, length, trail=10):
    """
    Spaghetti to try and dissolve the column vertically by 'attacking' each node
    top to bottom until it 'dies'.

    Ideally, it will adhere to the desired length given the framerate
    _but that's just an implmentation detail_.

    The concept of what a frame even is has been lost on me as I wrote the following lines.
    """

    total_health = len(collection[0].state) * Node.MAX_HEALTH * len(collection)
    hits_per_cycle = int((total_health / (length * FRAMERATE)) + 1)

    start = 0
    while start < len(collection):
        try:
            hits = 0
            for i in range(start, len(collection)):
                for j in range(start, min(i + trail, len(collection))):
                    if hits == hits_per_cycle:
                        raise BreakIt
                    else:
                        if r.randint(0, 1) == 0:
                            node = collection[j]
                            if not node.dead:
                                node.attack()
                                hits += 1
                            if node.dead:
                                if j == start:
                                    start += 1
                                raise BreakIt
            raise BreakIt
        except BreakIt:
            for node in collection:
                if not node.healthy:
                    node.update_state()
            hits = 0
            yield


def dissolveV2(collection, allow_linger=False, wipe=True):
    """
    A more emergent method of dissolving the collection.
    """

    dead = 0
    while dead < len(collection):
        for node in collection:
            if not node.dead:
                if not node.healthy:
                    if allow_linger and node.health == 1 and r.random() > 0.25:
                        pass
                    # elif allow_linger and 2 < node.health < 15 and r.random() > 0.6:
                    #     pass
                    # elif allow_linger and 16 < node.health < 35 and r.random() > 0.8:
                    #     pass
                    else:
                        node.attack()
                if node.healthy:
                    node.attack(max(1, int(len(node.source) / 8)))
                    if wipe:
                        break
                if node.dead:
                    dead += 1
        yield


def print_column(column):
    cls()
    print("\n".join(map(repr, column)))
    # print(f"Frame {frame}")
    sleep(1 / (FRAMERATE * 1.5))


def vertical_destruct(
    template, random=False, width=8, height=30, blocks=False, theme=THEME_STD
):
    """
    Drives the vertical destruct methods
    """

    if blocks:
        column = generate_column(width=width, height=height, theme=theme)
    else:
        column = generate_column(
            template=template, random=random, height=height, theme=theme
        )

    d = dissolveV2(column, allow_linger=True)

    d.send(None)
    frame = 1
    for _ in d:
        # print_column(column)
        cls()
        print("\n".join(map(repr, column)))
        print(f"Frame {frame}")
        sleep(1 / (FRAMERATE * 1.5))
        frame += 1

FRAMERATE = 20
def main():
    # demo()
    vertical_destruct(
        template=[0,0,0,0,0,0,0,0],
        random=False,
        width=12,
        height=25,
        blocks=False,
        theme=THEME_LOW_HEALTH,
    )


if __name__ == "__main__":
    main()
