from __future__ import print_function
from PIL import Image, ImageDraw
from pathlib import Path
import os


def ascii(fname, colour, resolution, background):
    lum = True
    rgb = False

    if background == 1:
        bg_colour = 255
        fill_colour = 0
    else:
        bg_colour = 0
        fill_colour = 255
    
    lum_dir = str(Path('./out/lum/').resolve())
    rgb_dir = str(Path('./out/rgb/').resolve())

    if colour == 1:
        lum = False
        rgb = True
    elif colour == 3:
        rgb = True

    ascii_12 = [".", "-", ";", "=", "*", "I", "V", "F", "X", "%", "N", "@"]

    img_rgb = Image.open("./in/" + fname)

    spacing = 10

    ratio = 12 - (resolution * 3)

    w = int(img_rgb.size[0] / ratio)
    h = int(img_rgb.size[1] / ratio)

    img_lum = img_rgb.resize((w, h)).convert("L")

    if rgb:
        img_rgb = img_rgb.resize((w, h))

    if lum:
        lum_out = Image.new("L", (w * spacing, h * spacing), color=bg_colour)
        lum_text = ImageDraw.Draw(lum_out)

    if rgb:
        rgb_out = Image.new(
            "RGB", (w * spacing, h * spacing), color=(bg_colour, bg_colour, bg_colour)
        )
        rgb_text = ImageDraw.Draw(rgb_out)

    lum_map = []
    rgb_map = []

    if background == 1:
        for y in range(0, h):
            lum_row = []
            for x in range(0, w):
                lum_row.append(11 - int(img_lum.getpixel((x, y)) / 23.2))
            lum_map.append(lum_row)
    else:
        for y in range(0, h):
            lum_row = []
            for x in range(0, w):
                lum_row.append(int(img_lum.getpixel((x, y)) / 23.2))
            lum_map.append(lum_row)

    if rgb:
        for y in range(0, h):
            rgb_row = []
            for x in range(0, w):
                rgb_row.append(img_rgb.getpixel((x, y)))
            rgb_map.append(rgb_row)

    for y in range(0, h):
        for x in range(0, w):
            if lum:
                lum_text.text(
                    (x * spacing, y * spacing),
                    ascii_12[lum_map[y][x]],
                    fill=fill_colour,
                )
            if rgb:
                rgb_text.text(
                    (x * spacing, y * spacing),
                    ascii_12[lum_map[y][x]],
                    fill=(rgb_map[y][x]),
                )

    if lum:
        lum_out.save(f'{lum_dir}/{fname}')
        print("Saved: " + file + " (B&W)")
    if rgb:
        rgb_out.save(f'{rgb_dir}/{fname}')
        print("Saved: " + file + " (RGB)")


def setup():
    global filelist, colour, resolution, background
    Path("./in").mkdir(parents=True, exist_ok=True)
    Path("./out/lum/").mkdir(parents=True, exist_ok=True)
    Path("./out/rgb/").mkdir(parents=True, exist_ok=True)
    filelist = os.listdir(os.path.dirname(os.path.realpath(__file__)) + "./in/")
    colour = input("Colour Mode? '1' - RGB, '2' - BW or '3' - both\n")
    resolution = input("Resolution? '1' - low, '2' - medium, '3' - high\n")
    background = input("Text/Background Colour? '1' - black/colour text on white, '2' - white/colour text on black\n")


if __name__ == "__main__":
    setup()   
    for file in filelist:
        ascii(file, int(colour), int(resolution), int(background))
