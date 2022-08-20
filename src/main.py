import sys
from modules.ascii import AsciiArt
from modules.parameter import getParameter,isParamValid, getParameterDict, PARAMS_ERRROR

def Main(args:list) -> None:

    Params = args[1:]
    if( len(args) == 1 ):Params = getParameter() 

    if( not isParamValid(Params) ):
        print(PARAMS_ERRROR)
        return

    Params = getParameterDict(Params)
    ASCII = AsciiArt(Params)
    ASCII.Start()

if(__name__ == "__main__"):Main(sys.argv)