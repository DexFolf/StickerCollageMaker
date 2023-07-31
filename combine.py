from wand.image import Image
from wand.color import Color
import math
import os
import string

def exitMsg():
    print('\nExiting...')
    exit()

def invalidInput(reason):
    match reason:
        case 'colour':
            print('\nERROR: Invalid input. Expected a valid HEX colour code.')
        case 'int':
            print('\nERROR: Invalid input. Expected a positive number with no decimals.')
        case 'images':
            print('\nERROR: No valid PNGs were found in the current directory.')
    exitMsg()

def isValidHex(s):
    if (not(len(s) == 3 or len(s) == 6)):
        return False
    return all(c in string.hexdigits for c in s)

def verifyValue(value,expected):
    match expected:
        case 'int':
            if not value.isnumeric():
                invalidInput('int')
            else:
                return int(value)
        case 'colour':
            if not isValidHex(value):
                invalidInput('colour')
        case 'images':
            if len(value) == 0:
                invalidInput('images')


print('\nSticker collage creation script by Dex Blueberry @ https://dexblueberry.xyz')
print('\nPlace this executable inside the directory of which you wish to create a collage.\nIt will create (and overwrite!) a file called \"output.png\" in the same directory.\n')

#Request values
print('\nInput a HEX background colour for the image:')
try:
    bgcolour = str(input('#'))
except KeyboardInterrupt:
    exitMsg()
verifyValue(bgcolour,'colour')
bgcolour = '#'+bgcolour

print('\nInput a HEX background colour for the stickers:')
try:
    stickercolour = str(input('#'))
except KeyboardInterrupt:
    exitMsg()
verifyValue(stickercolour,'colour')
stickercolour = '#'+stickercolour

print('\nInput sticker size (512):')
try:
    stickersize = input()
except KeyboardInterrupt:
    exitMsg()
if stickersize == '':
    stickersize = '512'
stickersize = verifyValue(stickersize,'int')

print('\nInput amount of pixels to pad AROUND each sticker (10):')
try:
    paddingouter = input()
except KeyboardInterrupt:
    exitMsg()
if paddingouter == '':
    paddingouter = '10'
paddingouter = verifyValue(paddingouter,'int')

print('\nInput amount of pixels to pad INSIDE each sticker (5):')
try:
    paddinginner = input()
except KeyboardInterrupt:
    exitMsg()
if paddinginner == '':
    paddinginner = '5'
paddinginner = verifyValue(paddinginner,'int')

print('\nHow many columns should there be? (0 = auto):')
try:
    columns = input()
except KeyboardInterrupt:
    exitMsg()
if columns == '':
    columns = '0'
columns = verifyValue(columns,'int')

print('\nProcessing...')

#Find every image in the current directory and shrink them to the specified dimensions
images = []
for file in os.listdir('./'):
    if file.endswith('.png') and file != 'output.png':
        images.append(Image(filename=file))
        images[-1].transform(resize="%dx%d>" % (stickersize, stickersize))
verifyValue(images,'images')

#If user didn't specify an amount of columns, find the square root of the total images then round up
if columns == 0 :
    columns = math.ceil(math.sqrt(len(images)))

montage = Image()
stickercanvas = []
outputfile = 'output.png'

#For every sticker, create a background image with the specified dimensions and colour, then layer the sticker ontop of it
for sticker in images:
    stickercanvas.append(Image(width=stickersize+(paddinginner*2), height=stickersize+(paddinginner*2), background=Color(stickercolour)))
    stickercanvas[-1].composite(sticker, left=int((stickercanvas[-1].width-sticker.width)/2), top=int((stickercanvas[-1].height-sticker.height)/2))
    montage.image_add(stickercanvas[-1])

#Create the actual final collage and output it
montage.background_color = bgcolour
montage.montage(tile=str(columns)+'x0',thumbnail=str(stickersize+(paddinginner*2))+'x'+str(stickersize+(paddinginner*2))+'^+'+str(paddingouter)+'+'+str(paddingouter))
montage.border(bgcolour,int(paddingouter/2),int(paddingouter/2))
montage.save(filename=outputfile)

print('\nExecution has finished. Check the directory for a file called \"output.png\"')