#Importing Library
from PIL import Image
from sys import argv

# read file that user wants converted from command line. If file can't be read, assign 
# the file to a file in the directory
try:
    txt=open(argv[1], "r")
except FileNotFoundError as e:
    print(e)
    print(f"dummy.txt being used for read")

    # if you'd rather not use the command line, put the path to your file here
    txt=open("dummy.txt", "r")   # path of your text file


BG=Image.open("myfont/bg.png") #path of page(background)photo (I have used blank page)
sheet_width=BG.width
gap, ht = 0, 0



for i in txt.read().replace("\n",""):
        cases = Image.open("myfont/{}.png".format(str(ord(i))))
        BG.paste(cases, (gap, ht))
        size = cases.width
        height=cases.height
        #print(size)
        gap+=size

        if sheet_width < gap or len(i)*115 >(sheet_width-gap):
            gap,ht=0,ht+140

print(gap)
print(sheet_width)
BG.show()

