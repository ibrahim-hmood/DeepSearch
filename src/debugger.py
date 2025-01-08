import inspect

class DebuggerColors:
    OKCYAN = '\033[96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'

class Debugger:
    """
    warn: displays a warning alongside calling function
    @param message: warning message(s) to be printed
    """
    def warn(self, message):
        #Print the message as warning
            #Get the calling function
        caller = inspect.stack()[1].function
            #And print the warning message
        print(DebuggerColors.WARNING + "[WARNING] {}: {}".format(caller, message))
    
    """
    debug: displays a debug message alongside calling function
    @param message: debug message(s) to be printed
    """
    def debug(self, message):
        #Print the message as a debug message
            #Get the calling function
        caller = inspect.stack()[1].function
            #And print the debug message
        print(DebuggerColors.OKCYAN + "[DEBUG] {}: {}".format(caller, message))
    
    """
    error: displays a error message alongside calling function
    @param message: error message(s) to be printed
    """
    def error(self, message):
        #Print the message as an error
            #Get the calling fuction
        caller = inspect.stack()[1].function
            #And print everything
        print(DebuggerColors.FAIL + "[ERROR] {}: {}".format(caller, message))
