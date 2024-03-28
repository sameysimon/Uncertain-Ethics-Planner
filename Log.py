from datetime import datetime
class Logger:
    history = []
    silent = False
    def add(new):
        if Logger.silent:
            return
        Logger.history.append(new)
    
    def ToString():
        s = ""
        for l in Logger.history:
            s += l
        return s

    def clear():
        Logger.history = []

    def FlushToFile():
        f = open('TrapTest.txt', 'a')
        f.write(Logger.ToString())
        f.close()
        Logger.clear()
