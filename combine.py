from wand.image import Image
from wand.color import Color
import sys
import math
import os
import string

errorMessages = {
    'colour': "Invalid input. Expected a valid HEX colour code.",
    'int': "Invalid input. Expected a positive number with no decimals.",
    'images': "No valid PNGs were found in the current directory.",
}

def isValidHex(s):
    return len(s) in (3, 6) and all(c in string.hexdigits for c in s)

def exitValueError(type):
    sys.exit("ERROR:" + errorMessages[type] + "\nExiting...")

def verifyValue(value, type):
    match type:
        case 'int':
            return int(value) if value.isnumeric() else exitValueError(type)
        case 'colour':
            return value if isValidHex(value) else exitValueError(type)
        case 'images':
            return value if len(value) > 0 else exitValueError(type)

def inputValue(prompt, type, default):
    print(prompt)
    try:
        value = input('#' if type == 'colour' else '')
    except KeyboardInterrupt:
        sys.exit("Interrupted")
    if value == '':
        value = default
    return verifyValue(value,type)

print("""
Sticker collage creation script by Dex Blueberry @ https://dexblueberry.xyz
Place this executable inside the directory of which you wish to create a collage.
It will create (and overwrite!) a file called "output.png" in the same directory.""")

#Request values
bgcolour = '#' + inputValue('\nInput a HEX background colour for the image:', 'colour', '')
stickercolour = '#' + inputValue('\nInput a HEX background colour for the stickers:', 'colour', '')
stickersize = inputValue('\nInput sticker size (512):', 'int', '512')
paddingouter = inputValue('\nInput amount of pixels to pad AROUND each sticker (10):', 'int', '10')
paddinginner = inputValue('\nInput amount of pixels to pad INSIDE each sticker (5):', 'int', '5')
columns = inputValue('\nHow many columns should there be? (0 = auto):', 'int', '0')

print('\nProcessing...')

#Find every image in the current directory and shrink them to the specified dimensions
images = []
for file in sorted(os.listdir('./')):
    if file.endswith('.png') and file != 'output.png':
        images.append(Image(filename=file))
        images[-1].transform(resize="{0}x{0}>".format(stickersize))
verifyValue(images,'images')

#If user didn't specify an amount of columns, find the square root of the total images then round up
if columns == 0 :
    columns = math.ceil(math.sqrt(len(images)))

montage = Image()
stickercanvas = []

#For every sticker, create a background image with the specified dimensions and colour, then layer the sticker ontop of it
for sticker in images:
    stickercanvas.append(Image(width=stickersize+(paddinginner*2), height=stickersize+(paddinginner*2), background=Color(stickercolour)))
    stickercanvas[-1].composite(sticker, left=int((stickercanvas[-1].width-sticker.width)/2), top=int((stickercanvas[-1].height-sticker.height)/2))
    montage.image_add(stickercanvas[-1])

#Create the actual final collage and output it
montage.background_color = bgcolour
montage.montage(tile=str(columns)+'x0',thumbnail=str(stickersize+(paddinginner*2))+'x'+str(stickersize+(paddinginner*2))+'^+'+str(paddingouter)+'+'+str(paddingouter))
montage.border(bgcolour,int(paddingouter/2),int(paddingouter/2))
montage.save(filename='output.png')

print('\nExecution has finished. Check the directory for a file called \"output.png\"')