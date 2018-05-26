from __future__ import print_function
from PIL import Image,ImageDraw
import os

filelist = os.listdir("D:/Documents/GitHub/Projects/Personal/ASCII Generator/in/")

def ascii(fname, colour, resolution):
    lum = True
    rgb = False
    
    lum_dir = os.path.dirname(__file__) + 'out/lum/'
    rgb_dir = os.path.dirname(__file__) + 'out/rgb/'

    if not os.path.exists(lum_dir):
        os.makedirs(lum_dir)

    if not os.path.exists(rgb_dir):
        os.makedirs(rgb_dir)

    if(colour == 1):
        lum = False
        rgb = True
    elif(colour == 3):
        rgb = True

    ascii_12 = ['.', '-', ';', '=', '*', 'I', 'V', 'F', 'X', 'N', '%', '@']

    img_rgb = Image.open("D:/Documents/GitHub/Projects/Personal/ASCII Generator/in/" + fname)

    spacing = 10

    ratio = 12-(resolution*3);

    w = int(img_rgb.size[0]/ratio)
    h = int(img_rgb.size[1]/ratio)

    img_lum = img_rgb.resize((w, h)).convert("L")

    if(rgb):
        img_rgb = img_rgb.resize((w, h))

    if(lum):
        lum_out = Image.new('L', (w*spacing, h*spacing), color = 255)
        lum_text = ImageDraw.Draw(lum_out)
      
    if(rgb):
        rgb_out = Image.new('RGB', (w*spacing, h*spacing), color = (255, 255, 255))
        rgb_text = ImageDraw.Draw(rgb_out)
        
    lum_map = []
    rgb_map = []
    
    for y in range(0, h):
        lum_row = []
        for x in range(0, w):
            lum_row.append(11-round(img_lum.getpixel((x,y))/23.2))     
        lum_map.append(lum_row)
    
    if(rgb):
        for y in range(0, h):
            rgb_row = []
            for x in range(0, w): 
                rgb_row.append(img_rgb.getpixel((x,y)))    
            rgb_map.append(rgb_row)

    for y in range(0, h):
        for x in range(0, w):
            if(lum):
                lum_text.text((x*spacing, y*spacing), ascii_12[lum_map[y][x]], fill=0)
            if(rgb):
                rgb_text.text((x*spacing, y*spacing), ascii_12[lum_map[y][x]], fill=(rgb_map[y][x]))

    if(lum):
        lum_out.save(lum_dir + fname)
        print("Saved: " + file + "(B&W)")
    if(rgb):
        rgb_out.save(rgb_dir + fname)
        print("Saved: " + file + "(RGB)")

colour = input("Colour Mode? '1' - RGB, '2' - BW or '3' - both\n").lower()
resolution = input("Resolution? '1' - low, '2' - medium, '3' - high\n").lower()

for file in filelist:
    ascii(file, int(colour), int(resolution))
