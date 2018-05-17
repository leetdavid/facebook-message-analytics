def hasParam(argv, howToUse = None):
    if len(argv) > 1:
        return True
    else:
        if howToUse:
            print(howToUse)
        return False