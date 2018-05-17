import os

def hasParam(argv, howToUse = None):
    if len(argv) > 1:
        return len(argv)
    else:
        if howToUse:
            print(howToUse)
        return False

def createDirectories(filepath):
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc: #Guard Against Race Condition
            if exc.errno != errno.EEXIST:
                raise