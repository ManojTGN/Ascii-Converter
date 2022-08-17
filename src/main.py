import os
import sys
from PIL import Image,ImageFont,ImageDraw

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: print()

def isParamValid(args) -> bool:

    if(len(args) <= 1):return False

    if(not isinstance(args[1], str)):return False
    if(len(args) == 2):return True

    if(not args[2].isnumeric() ):return False
    if(len(args) == 3):return True

    if(not args[3].isnumeric() ):return False
    if(len(args) == 4):return True

    if(not isinstance(args[4], str)):return False
    return True

def loadParams(args:list) -> None:
    
    if(len(args) <= 1):return
    OPTIONS['inputFileLocation'] = args[1]

    if(len(args) >= 3):OPTIONS['renderQuality'] = int(args[2])
    else:OPTIONS['renderQuality'] = 100

    if(len(args) >= 4):OPTIONS['renderMode'] = int(args[3])
    else:OPTIONS['renderMode'] = 0

    if(len(args) >= 5):OPTIONS['outputFileLocation'] = args[4]
    else:OPTIONS['outputFileLocation'] = os.getcwd()

def loadImageCharSet(IMAGE) -> list:
    CHARSET = []
    for x in range(IMAGE.width):
        CHARSET.append("")
        for y in range(IMAGE.height): 
            CHARSET[-1] += RENDER_MODES[OPTIONS['renderMode']][
                map_( 
                    IMAGE.getpixel((x,y)),0,255,0, len(RENDER_MODES[OPTIONS['renderMode']]) - 1
                )
            ]


    return CHARSET

def makeImage(CHARSET:list,frameNumber:int = 1,totalFrames:int = 1) -> Image:

    FONT = ImageFont.truetype("src\\fonts\\0.ttf", 16)
    width,height = FONT.getsize('A')
    kerning = 2

    IMAGE = Image.new('RGB',(width*len(CHARSET[0])*kerning,height*len(CHARSET)))
    DRAW = ImageDraw.Draw(IMAGE)
    for index,LINE in enumerate(CHARSET):
        printProgressBar(index, len(CHARSET)-1, prefix = f'Frame[{frameNumber}/{totalFrames}]:', suffix = 'Complete', length = 10)
        
        #DRAW.text((0, index*height),LINE,(255,255,255),font=FONT)
        for idx,CHAR in enumerate(LINE):
            DRAW.text((idx*width*kerning, index*height),CHAR,(255,255,255),font=FONT)
    
    return IMAGE

def map_(value, leftMin, leftMax, rightMin, rightMax) -> int:

    return int(rightMin + ((float(value - leftMin) / float((leftMax - leftMin))) * (rightMax - rightMin)))

def Main(args:list) -> None:

    if(len(args) <= 1 or not isParamValid(args)): 
        print("Invalid Parameter Specified!")
        return
    
    if(True): #Todo: If The File Is An Image
        loadParams(args)
        IMAGE = Image.open(OPTIONS['inputFileLocation']).convert('L')
        CHARSET = loadImageCharSet(IMAGE)
        IMAGE = makeImage(CHARSET)
        IMAGE.save(OPTIONS['outputFileLocation']+"\\Output.jpg")

RENDER_MODES = [
    "Ñ@#W$9876543210?!abc;:+=-,._ ",
    "",
    "",
    ""
]

OPTIONS = {
    'renderQuality':100,
    'renderMode':0,
    'inputFileLocation':'',
    'outputFileLocation':''
}

if(__name__ == "__main__"):
    Main(sys.argv)