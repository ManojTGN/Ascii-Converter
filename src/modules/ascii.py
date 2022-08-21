import urllib.request
from modules.parameter import isUrl
from PIL import Image,ImageFont,ImageDraw

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

        # Print The Bar
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        
        # Print New Line on Complete
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

    """
        Convert each pixel to intensity value (0-255) 
        and mapped to the rendermode's ascii characters
        @params:
            IMAGE     - Required  :  The Input Image (Image)
    """
    def loadImageCharSet(self,IMAGE:Image.Image) -> list:

        # List Of Strings with Ascii Characters
        CHARSET = []

        # Looping Throught All The Pixels In The
        # Image By Height And Width
        for x in range(IMAGE.height):

            # Appending A Empty String And Looping Throught
            # The (X axis) Of The Image And Appending The
            # Values To This String
            CHARSET.append("")
            for y in range(IMAGE.width):

                # Adding The AsciiArt Char To The Last String Of The List
                # According To The Pixel Value (0-255)
                CHARSET[-1] += self.RENDER_MODES[self.OPTIONS['renderMode']][
                    map_( 
                        IMAGE.getpixel((y,x)),0,255,0, len(self.RENDER_MODES[self.OPTIONS['renderMode']]) - 1
                    )
                ]
        
        return CHARSET

    """
        Resize The Image To The "RenderQuality" Specified By The User
        In Percentage (0-100)
        @params:
            IMAGE     - Required  :  The Input Image (Image)
    """
    def resizeToRenderQuality(self,IMAGE:Image.Image) -> Image.Image:

        # Converting the percentage to the value and resizing 
        # the image and returning it
        return IMAGE.resize( 
            ( int( 
                (IMAGE.width/100)*self.OPTIONS['renderQuality']
            ) ,
            int(
                (IMAGE.height/100)*self.OPTIONS['renderQuality']
            ) ) 
        )
    
    """
        Drawing/ Writing The Charset Into A Black Image
        @params:
            CHARSET     - Required  :  The Charset List That Returned From loadImageCharSet() function (List)
    """
    def makeImage(self,CHARSET:list) -> Image.Image:
        
        # Loading the JetbrainMono font else loading the
        # system default font
        try:FONT = ImageFont.truetype("src\\asserts\\font.ttf", 16)
        except:FONT = ImageFont.load_default()

        # Getting the width and height of a single character of the font
        # and setting the kerning(TextSpacing)
        width,height = FONT.getbbox('A')[2:]
        kerning = 2

        # Creating an image with the width and height
        IMAGE = Image.new('RGB',(width*len(CHARSET[0])*kerning,height*len(CHARSET)))

        # Making The Image Drawable To Write Text In It
        DRAW = ImageDraw.Draw(IMAGE)

        # Looping through the CHARSET
        for index,LINE in enumerate(CHARSET):

            # Updating The Progress Bar
            printProgressBar(index, len(CHARSET)-1, prefix = f'Rendering:', suffix = 'Complete', length = 15)
            
            # Looping Through Each Character In The Line
            # And Placing The Character With Kerning
            for idx,CHAR in enumerate(LINE):
                DRAW.text((idx*width*kerning, index*height),CHAR,(255,255,255),font=FONT)
            """ DRAW.text((0, index*height),LINE,(255,255,255),font=FONT) """
        
        return IMAGE
    
    """
        Start converting the image to the asciiart image
    """
    def Start(self):

        # Checking if the fileLocation is an url or not
        if(isUrl(self.OPTIONS['inputFileLocation'])):

            # Downloading the image and saving it as tmp.png and loading
            # the image then converting the image to GreyScale image
            try:
                urllib.request.urlretrieve(self.OPTIONS['inputFileLocation'],'tmp.png')
                IMAGE = Image.open('Input.png').convert('L')
            except:
                print("Unable to download/open the image!")
                return

        # if not url then it must be a systempath
        else:

            # loading the image and converting it to an greyscale image
            try:IMAGE = Image.open(self.OPTIONS['inputFileLocation']).convert('L')
            except:
                print("Unable to open the image!")
                return

        # Resizing the image to the user specified renderquality(0-100)
        IMAGE = self.resizeToRenderQuality(IMAGE)

        # converting the resized image to the Ascii Characters List 
        CHARSET = self.loadImageCharSet(IMAGE)

        # Now making a new image with the charset made
        IMAGE = self.makeImage(CHARSET)

        # Saving the image to the output location
        IMAGE.save(self.OPTIONS['outputFolderLocation']+"\\output.jpg",optimize=True,quality=self.OPTIONS['outputQuality'])