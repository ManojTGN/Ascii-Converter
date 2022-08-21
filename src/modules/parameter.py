import os
import requests
from os import path

# To Store Parameter Error
PARAMS_ERRROR = ''

"""
    To Check If It Is An System Directory/Path
    @params:
        location - Required  : Path-To-File/Folder (str)
"""
def isLocalPath(location:str) -> bool:

    return path.exists(location)

"""
    To Check If It Is An URL
    @params:
        url - Required  :  URL (str)
"""
def isUrl(url:str) -> bool:

    try:
        r = requests.head(url)
        return r.status_code == requests.codes.ok
    except: return False

"""
    Get All Parameters From The
    User In The Terminal
"""
def getParameter() -> list:
    
    PARAMETER = []

    # Input File Location (no default value) 
    PARAMETER.append(input("Input File Location:"))
    
    # Render Quality (default: 100)
    PARAMETER.append(input("RenderQuality[1-100] (100):"))
    if(PARAMETER[-1] == "" or PARAMETER[-1] == " "):PARAMETER[-1] = '100'

    # RenderMode (default: 0)
    PARAMETER.append(input("RenderMode[0-3] (0):"))
    if(PARAMETER[-1] == "" or PARAMETER[-1] == " "):PARAMETER[-1] = '0'

    # OutputQuality (default: 100)
    PARAMETER.append(input("OutputQuality[1-100] (100):"))
    if(PARAMETER[-1] == "" or PARAMETER[-1] == " "):PARAMETER[-1] = '100'

    # Output Folder Location (current Dir '.')
    PARAMETER.append(input(f"Output Folder Location ({os.getcwd()}):"))
    if(PARAMETER[-1] == "" or PARAMETER[-1] == " "):PARAMETER[-1] = os.getcwd()

    return PARAMETER

"""
    Validating The Parameters
    @params:
        PARAMETER - Required  :  The Arguments Specified By The User (List)
"""
def isParamValid(PARAMETER:list) -> bool:
    global PARAMS_ERRROR

    # Checking If The Input File Location Is An SystemPath Or URL
    if( len(PARAMETER) == 0 or (not isLocalPath(PARAMETER[0]) and not isUrl(PARAMETER[0])) ):
        PARAMS_ERRROR = 'Invalid InputFileLocation At 1st Parameter'
        return False
    if(len(PARAMETER) == 1):return True

    # Checking If The RenderQuality Can Be Converted To Int And Ranged From 1-100
    if(not PARAMETER[1].isnumeric() and (int(PARAMETER[1]) >0 and int(PARAMETER[1]) <= 100) ):
        PARAMS_ERRROR = 'Invalid RenderQuality At 2nd Parameter'
        return False
    if(len(PARAMETER) == 2):return True

    # Checking If The RenderMode Can Be Converted To Int And Ranged From 0-2
    if(not PARAMETER[2].isnumeric() and (int(PARAMETER[2]) >=0 and int(PARAMETER[2]) < 3) ):
        PARAMS_ERRROR = 'Invalid RenderMode At 3rd Parameter'
        return False
    if(len(PARAMETER) == 3):return True

    # Checking If The OutputQuality Can Be Converted To Int And Ranged From 1-100
    if(not PARAMETER[3].isnumeric() and (int(PARAMETER[3]) >0 and int(PARAMETER[3]) <= 100)):
        PARAMS_ERRROR = 'Invalid OutputQuality At 4th Parameter'
        return False
    if(len(PARAMETER) == 4):return True

    # Checking If The OutputFileLocation Is A Valid Path
    if(not isLocalPath(PARAMETER[4])):
        PARAMS_ERRROR = 'Invalid OutputFileLocation At 5th Parameter'
        return False
    return True

"""
    Making The Parameter List To A Dict
    @params:
        PARAMETER - Required  :  The Arguments Specified By The User (List)
"""
def getParameterDict(PARAMETER:list) -> dict:

    # Making The Dict With Default Values
    OPTIONS = {
        'renderQuality':100,
        'outputQuality':100,
        'renderMode':0,
        'inputFileLocation':'',
        'outputFolderLocation':os.getcwd()
    }

    # Storing The Parameters According To The Dict
    OPTIONS['inputFileLocation'] = PARAMETER[0]
    if(len(PARAMETER) >= 2):OPTIONS['renderQuality'] = int(PARAMETER[1])
    if(len(PARAMETER) >= 3):OPTIONS['renderMode'] = int(PARAMETER[2])
    if(len(PARAMETER) >= 4):OPTIONS['outputQuality'] = int(PARAMETER[3])
    if(len(PARAMETER) >= 5):OPTIONS['outputFolderLocation'] = PARAMETER[4]

    return OPTIONS