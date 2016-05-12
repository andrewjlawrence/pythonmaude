# Copyright 2016 Andrew Lawrence

# Abstract syntax tree
class AST:
    pass

# System commands
class InCommand(AST):
    def __init__(self, filename):
        self.filename = filename
    def __eq__(self, other):
        return self.filename == other.filename
    def __ne__(self, other):
        return not self.__eq__(other)

class LoadCommand(AST):
    def __init__(self, filename):
        self.filename = filename
    def __eq__(self, other):
        return self.filename == other.filename

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
    def __eq__(self, other):
        return self.filename == other.filename


class PushCommand(AST):
    def __init__(self, directory):
        self.directory = directory
    def __eq__(self, other):
        return self.filename == other.filename


class LsCommand(AST):
    def __init__(self, lsflags="", directory=""):
        self.lsflags = lsflags
        self.directory = directory
    def __eq__(self, other):
        return self.directory == other.directory and self.lsflags == other.lsflags

