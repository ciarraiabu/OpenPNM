
class Log():

    LOGGING_ENABLE = True

    ERROR_ENABLE = True
    INFO_ENABLE = True
    DEBUG_ENABLE = True

    def __init__(self, moduleName):
        self._moduleName = "[" + moduleName + "]"
        return True

    def isDebugEnable():
        return Log.DEBUG_ENABLE

    def error(s: str):
        if (Log.LOGGING_ENABLE is True) and (Log.ERROR_ENABLE is True):
            print("ERROR: " + str(s))

    def info(s: str):
        if (Log.LOGGING_ENABLE is True) and (Log.INFO_ENABLE is True):
            print("INFO: " + str(s))

    def debug(s: str):
        if (Log.LOGGING_ENABLE is True) and (Log.DEBUG_ENABLE is True):
            print("DEBUG: " + str(s))
    
    def warning(s: str):
        if (Log.LOGGING_ENABLE is True) and (Log.DEBUG_ENABLE is True):
            print("WARN: " + str(s))
