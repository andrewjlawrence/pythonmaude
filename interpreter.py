# Copyright 2016 Andrew Lawrence
import ast, maudeparser, pyparsing, sys, string
import os
from loader import Loader

directorystack = []


def onquit(quitcommand):
    sys.exit(0)


def onchangedirectory(cdcommand):
    if os.path.exists(cdcommand.path):
        os.chdir(cdcommand.path)
    else:
        print("Error invalid path")


def onload(loadcommand):

    maudeparser.module.parsefile(loadcommand.filename)



def onin(incommand):
    pass


def onpopd(popdcommand):
    pass


def onls(lscommand):
    if lscommand.path:
        if os.path.dirname(lscommand.path):
            print(*os.listdir(lscommand.path), sep='\n')
        else:
            print("Error invalid path")
    else:
        print(*os.listdir(os.getcwd()), sep='\n')


def onpwd(pwdcommand):
    print(os.getcwd())


def onpushd(pushdcommand):
    pass


def oneof(eofcommand):
    pass


def unimplemented():
    print("Unimplemented")

case = {ast.CommandType.quitcommand: onquit,
        ast.CommandType.cdcommand:   onchangedirectory,
        ast.CommandType.loadcommand: onload,
        ast.CommandType.incommand:   onin,
        ast.CommandType.popdcommand: onpopd,
        ast.CommandType.pwdcommand:  onpwd,
        ast.CommandType.pushcommand: onpushd,
        ast.CommandType.lscommand:   onls,
        ast.CommandType.eofcommand:  oneof}


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
while True:
    try:
        evaluator.eval(maudeparser.systemcommand.parseString(input("Maude> "))[0])
    except pyparsing.ParseException:
        print("Unknown command")
