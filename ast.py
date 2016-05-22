# Copyright 2016 Andrew Lawrence
from enum import Enum

class CommandType(Enum):
    incommand = 1
    loadcommand = 2
    quitcommand = 3
    eofcommand = 4
    popdcommand = 5
    pwdcommand = 6
    cdcommand = 7
    pushcommand = 8
    lscommand = 9

# Abstract syntax tree
class AST:
    pass

# System commands
class InCommand(AST):
    def __init__(self, filename):
        self.filename = filename
    def __eq__(self,other):
        return self.filename == other.filename
    def __ne__(self, other):
        return not self.__eq__(other)
    def commandtype(self):
        return CommandType.incommand

class LoadCommand(AST):
    def __init__(self, filename):
        self.filename = filename
    def __eq__(self, other):
        return self.filename == other.filename
    def commandtype(self):
        return CommandType.loadcommand

class QuitCommand(AST):
    def commandtype(self):
        return CommandType.quitcommand
    def __eq__(self,other):
        return True

class EofCommand(AST):
    def commandtype(self):
        return CommandType.eofcommand
    def __eq__(self,other):
        return True

class PopDCommand(AST):
    def commandtype(self):
        return CommandType.popdcommand
    def __eq__(self,other):
        return True


class PwdCommand(AST):
    def commandtype(self):
        return CommandType.pwdcommand
    def __eq__(self,other):
        return True

class CdCommand(AST):
    def __init__(self, directory):
        self.directory = directory
    def __eq__(self, other):
        return self.directory == other.directory
    def commandtype(self):
        return CommandType.cdcommand

class PushCommand(AST):
    def __init__(self, directory):
        self.directory = directory
    def __eq__(self, other):
        return self.directory == other.directory
    def commandtype(self):
        return CommandType.pushcommand

class LsCommand(AST):
    def __init__(self, lsflags="", directory=""):
        self.lsflags = lsflags
        self.directory = directory
    def __eq__(self, other):
        return self.directory == other.directory and self.lsflags == other.lsflags
    def commandtype(self):
        return CommandType.lscommand
