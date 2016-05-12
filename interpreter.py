# Copyright 2016 Andrew Lawrence
import ast,parser, pyparsing, sys

def eval(x):
    case = {
        ast.QuitCommand : sys.exit(0)
    }
    return case(x)

while (True):
    try:
        eval(parser.systemcommand.parseString(input(":-"))[0])
    except pyparsing.ParseException:
        print("Unknown command")