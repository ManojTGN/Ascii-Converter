import sys
from modules.ascii import AsciiArt
from modules.parameter import getParameter,isParamValid, getParameterDict, PARAMS_ERRROR

"""
    Main Function, Get And Validate The Parameter
    Then Start To Make The AsciiArt
    @params:
        args - Required  : Arguments In The Terminal (list)
"""
def Main(args:list) -> None:

    # Setting The Parameter To The Argument(args) Given
    # And Removing The First Element From It.
    Params = args[1:]

    # If The Length Of Argument(args) Is 1 Then There Is
    # No Parameter Specified And So Get Parameter
    if( len(args) == 1 ):Params = getParameter() 

    # After Parameter(Params) Is Ready Validate The
    # Parameters Given By The User
    if( not isParamValid(Params) ):

        # If The Parameter Is Invalid Then Printing
        # The Error And Exiting The Main Function
        print(PARAMS_ERRROR)
        return

    # Getting The Parameters In A Dict Type
    # And Starting The AsciiArt
    Params = getParameterDict(Params)
    ASCII = AsciiArt(Params)
    ASCII.Start()

# Calling The Main() Function With The Given 
# Arguments In The Terminal.
if(__name__ == "__main__"):Main(sys.argv)