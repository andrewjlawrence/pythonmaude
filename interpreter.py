# Copyright 2016 Andrew Lawrence
import ast,parser, pyparsing, sys

def eval(x):
    case = {
        ast.QuitCommand: sys.exit(0),
        ast.CdCommand(dir): print("Unimplemented"),
        ast.EofCommand: print("Unimplemented"),
        ast.InCommand: print("Unimplemented"),
        ast.LoadCommand: print("Unimplemented"),
        ast.LsCommand: print("Unimplemented"),
        ast.PopDCommand : print("Unimplemented"),
        ast.PushCommand: print("Unimplemented"),
        ast.PwdCommand: print("Unimplemented")
    }
    return case[type(x)]

while (True):
    try:
        eval(parser.systemcommand.parseString(input("Maude> "))[0])
    except pyparsing.ParseException:
        print("Unknown command")