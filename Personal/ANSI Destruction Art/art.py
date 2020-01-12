from node import Node
import colours as c
from time import sleep
from itertools import permutations
import os
import random

SEP = f"{c.ENDC} "
FRAMERATE = 30

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


def main():
    # demo()
    vertical_destruct(40)

def generate_column(set, size):
    perms = permutations(map(str, set))
    column = []
    for p in perms:
        column.append(Node("".join(p)))
        if len(column) == size:
            break

    return column

class BreakIt(Exception): pass

def dissolve(collection, length, trail=10):
    """
    Spaghetti to try and dissolve the column vertically by 'attacking' each node
    top to bottom until it 'dies'.

    Ideally, it will adhere to the desired length given the framerate
    _but that's just an implmentation detail_.

    The concept of what a frame even is has been lost on me as I wrote the following lines.
    """

    total_health = len(collection[0].state) * Node.MAX_HEALTH * len(collection)
    hits_per_cycle = int((total_health / (length * FRAMERATE))+1)

    start = 0
    while start < len(collection):
        try:
            hits = 0
            for i in range(start, len(collection)):
                for j in range(start, min(i+trail, len(collection))):
                    if hits == hits_per_cycle:
                        raise BreakIt
                    else:
                        if random.randint(0, 1) == 0:
                            node = collection[j]
                            if not node.dead:
                                node.hurt()
                                hits += 1
                            if node.dead:
                                if j == start:
                                    start += 1
                                raise BreakIt
            raise BreakIt
        except BreakIt:
            for node in collection:
                if not node.healthy:
                    node.update_stateV2()
            hits = 0
            yield 

def vertical_destruct(size):
    """
    Drives the vertical destruct methods
    """

    column = generate_column([1,2,3,4,5], size)

    d = dissolve(column, 2)

    d.send(None)
    frame = 1
    for _ in d:
        cls()
        print("\n".join(map(repr, column)))
        print(f"Frame {frame}")
        sleep(1/(FRAMERATE*1.5))
        frame += 1
    

if __name__ == "__main__":
    main()
