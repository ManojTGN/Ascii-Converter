import urllib.request
from PIL import Image,ImageFont,ImageDraw
from modules.parameter import isUrl

"""
    Terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        autosize    - Optional  : automatically resize the length of the progress bar to the terminal window (Bool)
"""
def printProgressBar (iteration:int, total:int, prefix:str = '', suffix:str = '', decimals:int = 1, length:int = 100, fill:str = '█', printEnd = "\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)

        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        if iteration == total: print()

"""
    Maps One Ranged Value To Another Ranged Value
    @params:
        value     - Required  : Value to be changed from range 1 to 2 (Int)
        leftMin   - Required  : Minimum of range one (Int)
        leftMax   - Optional  : Maximum of range one (Int)
        rightMin  - Optional  : Minimum of range two (Int)
        rightMax  - Optional  : Maximum of range two (Int)
"""
def map_(value, leftMin, leftMax, rightMin, rightMax) -> int:
    return int(rightMin + ((float(value - leftMin) / float((leftMax - leftMin))) * (rightMax - rightMin)))

class AsciiArt:

    # Renders Mode To Select The Characters
    # In The Ascii Art (0) is default
    RENDER_MODES = [
        "Ñ@#W$9876543210?!abc;:+=-,._ ",
        ":$#$:   \"4b. ':.",
        "██▓▓▒▒░░  ",
        ""
    ]


    """
        AsciiArt Init Function
        The Option Dict Must Contains
            renderQuality, outputQuality, renderMode
            inputFileLocation, outputFolderLocation
        @params:
            OPTIONS     - Required  :  Valid Argument Dict (Dict)
    """
    def __init__(self,OPTIONS) -> None:
        self.OPTIONS = OPTIONS


    def loadImageCharSet(self,IMAGE:Image.Image) -> list:
        CHARSET = []
        for x in range(IMAGE.height):
            CHARSET.append("")
            for y in range(IMAGE.width):
                CHARSET[-1] += self.RENDER_MODES[self.OPTIONS['renderMode']][
                    map_( 
                        IMAGE.getpixel((y,x)),0,255,0, len(self.RENDER_MODES[self.OPTIONS['renderMode']]) - 1
                    )
                ]
        return CHARSET

    def resizeToRenderQuality(self,IMAGE:Image.Image) -> Image.Image:
        return IMAGE.resize( 
            ( int( 
                (IMAGE.width/100)*self.OPTIONS['renderQuality']
            ) ,
            int(
                (IMAGE.height/100)*self.OPTIONS['renderQuality']
            ) ) 
        )
    
    def makeImage(self,CHARSET:list,frameNumber:int = 1,totalFrames:int = 1) -> Image.Image:

        try:FONT = ImageFont.truetype("src\\asserts\\font.ttf", 16)
        except:FONT = ImageFont.load_default()
        width,height = FONT.getbbox('A')[2:]
        kerning = 2

        IMAGE = Image.new('RGB',(width*len(CHARSET[0])*kerning,height*len(CHARSET)))
        DRAW = ImageDraw.Draw(IMAGE)
        for index,LINE in enumerate(CHARSET):
            printProgressBar(index, len(CHARSET)-1, prefix = f'Frame[{frameNumber}/{totalFrames}]:', suffix = 'Complete', length = 15)
            
            #DRAW.text((0, index*height),LINE,(255,255,255),font=FONT)
            for idx,CHAR in enumerate(LINE):
                DRAW.text((idx*width*kerning, index*height),CHAR,(255,255,255),font=FONT)
        
        return IMAGE
    
    def Start(self):

        if(isUrl(self.OPTIONS['inputFileLocation'])):
            try:
                urllib.request.urlretrieve(self.OPTIONS['inputFileLocation'],'Input.png')
                IMAGE = Image.open('Input.png').convert('L')
            except:
                print("Unable to download/open the image!")
                return
        else:
            try:IMAGE = Image.open(self.OPTIONS['inputFileLocation']).convert('L')
            except:
                print("Unable to open the image!")
                return

        IMAGE = self.resizeToRenderQuality(IMAGE)
        CHARSET = self.loadImageCharSet(IMAGE)

        IMAGE = self.makeImage(CHARSET)
        IMAGE.save(self.OPTIONS['outputFolderLocation']+"\\output.jpg",optimize=True,quality=self.OPTIONS['outputQuality'])