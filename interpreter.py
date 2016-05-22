# Copyright 2016 Andrew Lawrence
import ast,maudeparser,pyparsing,sys,string
import os

directorystack = []

def onQuit(quitcommand):
    sys.exit(0)

def onChangeDirectory(cdcommand):
    if (os.path.exists(cdcommand.path)):
        os.chdir(cdcommand.path)
    else:
        print("Error invalid path")


def onLoad(loadcommand):
    pass

def onIn(incommand):
    pass

def onPopd(popdcommand):
    pass

def onLs(lscommand):
    if lscommand.path:
        if os.path.dirn(lscommand.path):
            print(*os.listdir(lscommand.path), sep='\n')
        else:
            print("Error invalid path")
    else:
        print(*os.listdir(os.getcwd()), sep='\n')

def onPwd(pwdcommand):
    print(os.getcwd())

def onPushD(pushdcommand):
    pass

def onEOF(eofcommand):
    pass

def unimplemented():
    print("Unimplemented")

case = {ast.CommandType.quitcommand: onQuit,
        ast.CommandType.cdcommand:   onChangeDirectory,
        ast.CommandType.loadcommand: onLoad,
        ast.CommandType.incommand:   onIn,
        ast.CommandType.popdcommand: onPopd,
        ast.CommandType.pwdcommand:  onPwd,
        ast.CommandType.pushcommand: onPushD,
        ast.CommandType.lscommand:   onLs,
        ast.CommandType.eofcommand:  onEOF}

class CommandEvaluator:
    def __init__(self):
        self.lasterror = ""
    def eval(self, x):
        try:
            case[x.commandtype()](x)
        except SystemExit as s:
            raise s
        except:
            self.lasterror = ""

evaluator = CommandEvaluator()
while (True):
    try:
        evaluator.eval(maudeparser.systemcommand.parseString(input("Maude> "))[0])
    except pyparsing.ParseException:
        print("Unknown command")