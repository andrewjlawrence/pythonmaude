# Copyright 2016 Andrew Lawrence

# Abstract syntax tree
class AST:
    pass

# System command
class InCommand(AST):
    def __init__(self, filename):
        self.filename = filename

class LoadCommand(AST):
    def __init__(self, filename):
        self.filename = filename

class QuitCommand(AST):
    pass

class EofCommand(AST):
    pass

class PopDCommand(AST):
    pass

class PwdCommand(AST):
    pass

class CdCommand(AST):
    def __init__(self, directory):
        self.directory = directory

class PushCommand(AST):
    def __init__(self, directory):
        self.directory = directory

class LsCommand(AST):
    def __init__(self, lsflags="", directory=""):
        self.lsflags = lsflags
        self.directory = directory

