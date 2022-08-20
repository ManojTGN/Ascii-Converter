import os
import requests
from os import path

PARAMS_ERRROR = ''

def isLocalPath(location:str) -> bool:

    return path.exists(location)


def isUrl(url:str) -> bool:

    try:
        r = requests.head(url)
        return r.status_code == requests.codes.ok
    except: return False


def getParameter() -> list:
    
    PARAMETER = []
    PARAMETER.append(input("Input File Location:"))
    
    PARAMETER.append(input("RenderQuality[1-100] (100):"))
    if(PARAMETER[-1] == "" or PARAMETER[-1] == " "):PARAMETER[-1] = '100'

    PARAMETER.append(input("RenderMode[0-3] (0):"))
    if(PARAMETER[-1] == "" or PARAMETER[-1] == " "):PARAMETER[-1] = '0'

    PARAMETER.append(input("OutputQuality[1-100] (100):"))
    if(PARAMETER[-1] == "" or PARAMETER[-1] == " "):PARAMETER[-1] = '100'

    PARAMETER.append(input(f"Output Folder Location ({os.getcwd()}):"))
    if(PARAMETER[-1] == "" or PARAMETER[-1] == " "):PARAMETER[-1] = os.getcwd()

    return PARAMETER


def isParamValid(PARAMETER:list) -> bool:
    global PARAMS_ERRROR

    if( len(PARAMETER) == 0 or (not isLocalPath(PARAMETER[0]) and not isUrl(PARAMETER[0])) ):
        PARAMS_ERRROR = 'Invalid InputFileLocation At 1st Parameter'
        return False
    if(len(PARAMETER) == 1):return True


    if(not PARAMETER[1].isnumeric() and (int(PARAMETER[1]) >0 and int(PARAMETER[1]) <= 100) ):
        PARAMS_ERRROR = 'Invalid RenderQuality At 2nd Parameter'
        return False
    if(len(PARAMETER) == 2):return True


    if(not PARAMETER[2].isnumeric() and (int(PARAMETER[2]) >=0 and int(PARAMETER[2]) < 3) ):
        PARAMS_ERRROR = 'Invalid RenderMode At 3rd Parameter'
        return False
    if(len(PARAMETER) == 3):return True


    if(not PARAMETER[3].isnumeric() and (int(PARAMETER[3]) >0 and int(PARAMETER[3]) <= 100)):
        PARAMS_ERRROR = 'Invalid OutputQuality At 4th Parameter'
        return False
    if(len(PARAMETER) == 4):return True


    if(not isLocalPath(PARAMETER[4])):
        PARAMS_ERRROR = 'Invalid OutputFileLocation At 5th Parameter'
        return False
    return True


def getParameterDict(PARAMETER:list) -> dict:

    OPTIONS = {
        'renderQuality':100,
        'outputQuality':100,
        'renderMode':0,
        'inputFileLocation':'',
        'outputFolderLocation':os.getcwd()
    }

    OPTIONS['inputFileLocation'] = PARAMETER[0]
    if(len(PARAMETER) >= 2):OPTIONS['renderQuality'] = int(PARAMETER[1])
    if(len(PARAMETER) >= 3):OPTIONS['renderMode'] = int(PARAMETER[2])
    if(len(PARAMETER) >= 4):OPTIONS['outputQuality'] = int(PARAMETER[3])
    if(len(PARAMETER) >= 5):OPTIONS['outputFolderLocation'] = PARAMETER[4]

    return OPTIONS