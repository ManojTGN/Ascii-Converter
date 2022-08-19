import os
import sys

import requests
import urllib.request
from os import path
from enum import Enum
from PIL import Image,ImageFont,ImageDraw

class InputType(Enum):
    NONE = 0

    IMAGE_LINK = 1
    IMAGE_LOCATION = 2

    VIDEO_LINK = 3
    VIDEO_LOCATION = 4

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)

    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: print()

def map_(value, leftMin, leftMax, rightMin, rightMax) -> int:
    return int(rightMin + ((float(value - leftMin) / float((leftMax - leftMin))) * (rightMax - rightMin)))

def exists(path:str):
    r = requests.head(path)
    return r.status_code == requests.codes.ok

def isParamValid(args) -> bool:
    if( len(args) == 0 or (not path.exists(args[0]) and not exists(args[0])) ):return False

    if(path.exists(args[0])): OPTIONS['inputType'] = InputType.IMAGE_LOCATION
    elif(exists(args[0])): OPTIONS['inputType'] = InputType.IMAGE_LINK
    if(len(args) == 1):return True

    if(not args[1].isnumeric() and (int(args[1]) >0 and int(args[1]) <= 100) ):return False
    if(len(args) == 2):return True

    if(not args[2].isnumeric() and (int(args[2]) >=0 and int(args[2]) < len(RENDER_MODES)) ):return False
    if(len(args) == 3):return True

    if(not args[3].isnumeric() and (int(args[3]) >0 and int(args[3]) <= 100)):return False
    if(len(args) == 4):return True

    if(not path.exists(args[4])):return False
    return True

def loadParams(args:list) -> None:
    if(len(args) == 0):return

    OPTIONS['inputFileLocation'] = args[0]
    if(len(args) >= 2):OPTIONS['renderQuality'] = int(args[1])
    if(len(args) >= 3):OPTIONS['renderMode'] = int(args[2])
    if(len(args) >= 4):OPTIONS['outputQuality'] = int(args[3])
    if(len(args) >= 5):OPTIONS['outputFolderLocation'] = args[4]

def resizeToRenderQuality(IMAGE:Image.Image) -> Image.Image:
    return IMAGE.resize( 
        ( int( 
            (IMAGE.width/100)*OPTIONS['renderQuality']
        ) ,
        int(
            (IMAGE.height/100)*OPTIONS['renderQuality']
        ) ) 
    )

def loadImageCharSet(IMAGE:Image.Image) -> list:
    CHARSET = []
    for x in range(IMAGE.height):
        CHARSET.append("")
        for y in range(IMAGE.width):
            CHARSET[-1] += RENDER_MODES[OPTIONS['renderMode']][
                map_( 
                    IMAGE.getpixel((y,x)),0,255,0, len(RENDER_MODES[OPTIONS['renderMode']]) - 1
                )
            ]

    return CHARSET

def makeImage(CHARSET:list,frameNumber:int = 1,totalFrames:int = 1) -> Image.Image:
    FONT = ImageFont.truetype("src\\fonts\\0.ttf", 16)
    width,height = FONT.getbbox('A')[2:]
    kerning = 2

    IMAGE = Image.new('RGB',(width*len(CHARSET[0])*kerning,height*len(CHARSET)))
    DRAW = ImageDraw.Draw(IMAGE)
    for index,LINE in enumerate(CHARSET):
        printProgressBar(index, len(CHARSET)-1, prefix = f'Frame[{frameNumber}/{totalFrames}]:', suffix = 'Complete', length = 10)
        
        #DRAW.text((0, index*height),LINE,(255,255,255),font=FONT)
        for idx,CHAR in enumerate(LINE):
            DRAW.text((idx*width*kerning, index*height),CHAR,(255,255,255),font=FONT)
    
    return IMAGE

def Main(args:list) -> None:
    if(len(args) == 1 or not isParamValid(args[1:])): 
        print("Invalid Parameter Specified!")
        return
    
    loadParams(args[1:])
    if(True): #Todo: If The File Is An Image
        if(OPTIONS['inputType'] == InputType.IMAGE_LINK):
            try:
                urllib.request.urlretrieve(OPTIONS['inputFileLocation'],'Input.png')
                IMAGE = Image.open('Input.png').convert('L')
            except:
                print("Unable To Download/Open The Image!")
                return
        else:IMAGE = Image.open(OPTIONS['inputFileLocation']).convert('L')

        IMAGE = resizeToRenderQuality(IMAGE)
        CHARSET = loadImageCharSet(IMAGE)

        IMAGE = makeImage(CHARSET)
        IMAGE.save(OPTIONS['outputFolderLocation']+"\\output.jpg",optimize=True,quality=OPTIONS['outputQuality'])

RENDER_MODES = [
    "Ñ@#W$9876543210?!abc;:+=-,._ ",
    "",
    "",
    ""
]

OPTIONS = {
    'renderQuality':100,
    'outputQuality':100,
    'renderMode':0,

    'inputType':InputType.NONE,
    'inputFileLocation':'',
    'outputFolderLocation':os.getcwd()
}

if(__name__ == "__main__"):
    Main(sys.argv)