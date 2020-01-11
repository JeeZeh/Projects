from node import Node
import colours as c
from time import sleep
import os

SEP = f"{c.ENDC} "


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def demo(text, colours, framerate=20):
    while True:
        for _ in range(framerate):
            rows = []
            for i in range(0, 4):
                rows.append([Node(t, colour=c.UNDERLINE) for t in text])
                for n in rows[-1]:
                    n.set_health(4 - i)
                    n.set_colour(colours[i])
            output = "\n".join([SEP.join(map(repr, row)) for row in rows])
            cls()
            print(output)
            sleep(1 / framerate)


def main():
    text = input()
    if not text:
        text = "This is a demo\ntesting text destruction\nusing ANSI colours\nin a random but progressive style!".splitlines()
    else:
        text = text.split("  ")
    colours = [c.UNDERLINE, c.OKBLUE, c.WARNING, c.FAIL]
    demo(text, colours)


if __name__ == "__main__":
    main()
