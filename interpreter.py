# Copyright 2016 Andrew Lawrence
import ast,parser,pyparsing,sys,string
import os

def onQuit(quitcommand):
    sys.exit(0)

def onChangeDirectory(cdcommand):
    os.chdir(cdcommand.directory)

def onLoad(loadcommand):
    pass

def onIn(incommand):
    pass

def onPopd(popdcommand):
    pass

def onLs(lscommand):
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
        evaluator.eval(parser.systemcommand.parseString(input("Maude> "))[0])
    except pyparsing.ParseException:
        print("Unknown command")