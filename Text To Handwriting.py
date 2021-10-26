# Importing Library
from PIL import Image, ImageEnhance
from sys import argv
import numpy as np
import re #regex

# List of colors
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
purple = (142, 68, 173)

# if you'd rather not use the command line, put the path to your file here
fileName = "dummy.txt"  # path of your text file

color = black  # RGB Color, by default black


# read file that user wants converted from command line. If file can't be read, assign
# the file to a file in the directory
try:
    txt = open(argv[1], "r")
except IndexError:
    print("No file entered. Using default file...")
    txt = open(fileName, "r")
except FileNotFoundError:
    print("Could not find file. Using default file...")
    txt = open(fileName, "r")


# path of page(background)photo (I have used blank page)
BG = Image.open("myfont/bg.png")
sheet_width = BG.width
gap, ht = 0, 0

# for each letter in the uploaded txt file, read the unicode value and replace it with
# the corresponding handwritten file in the "myfont" folder.
lines = txt.readlines()
for line in lines:
    if re.search("txtColor=", line) != None: ##Check if flag color is set
        colortmp = line.split("=")[1].rstrip("\n")
        print(colortmp)
        if colortmp == "red": color = red
        if colortmp == "blue": color = blue
        if colortmp == "green": color = green
        if colortmp == "purple": color = purple
        if colortmp == "black": color = black
        continue
    for i in line:
        if(i == "\n"):
            print("Newline")  # Accepting newline
            gap, ht = 0, ht+140
            continue
        cases = Image.open("myfont/{}.png".format(str(ord(i))))
        cases = cases.convert("RGBA")

        #Add contrast to the image to make letters darkers
        enhancer = ImageEnhance.Contrast(cases)
        factor = 5
        im_output = enhancer.enhance(factor)
        data = np.array(im_output)
        red, green, blue, alpha = data.T

        #Getting black pixels
        black_areas = (red == 0) & (blue == 0) & (green == 0)
        data[..., :-1][black_areas.T] = black #Make the pixels black
        try:
            data[..., :-1][black_areas.T] = color #Change color of letter
        except:
            print("No change of color")
        cases = Image.fromarray(data)
        
        BG.paste(cases, (gap, ht))
        size = cases.width
        height = cases.height
        # print(size)
        print("Running...........")
        gap += size

        if sheet_width < gap or len(i)*115 > (sheet_width-gap):
            gap, ht = 0, ht+140

print(gap)
print(sheet_width)
BG.show()
