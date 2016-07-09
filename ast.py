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


# Identifier
class Ident(AST):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)


# Literal
class Literal(AST):
    def __init__(self, value):
        self.value = value


#
# Attributes
#
class AttributeType(Enum):
    assoc = 1
    comm = 2
    left = 3
    right = 4
    idem = 5
    iter = 6
    memo = 7
    ditto = 8
    config = 9
    obj = 10
    msg = 11
    metadata = 12
    strat = 13
    poly = 14
    frozen = 15
    prec = 16
    gather = 17
    format = 18
    special = 19
    unknown = 20


class Attributes(AST):
    def __init__(self, attributelist):
        self.attributelist = attributelist

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False


class MaudeAttribute(AST):
    def __init__(self, intype: AttributeType):
        self.attrtype = intype

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False


class Left(MaudeAttribute):
    def __init__(self, tree):
        MaudeAttribute.__init__(self, AttributeType.left)
        self.tree = tree


class Right(MaudeAttribute):
    def __init__(self, tree):
        MaudeAttribute.__init__(self, AttributeType.right)
        self.tree = tree


class MetaData(MaudeAttribute):
    def __init__(self, tree):
        MaudeAttribute.__init__(self, AttributeType.metadata)
        self.tree = tree


class Strat(MaudeAttribute):
    def __init__(self, listtree):
        MaudeAttribute.__init__(self, AttributeType.strat)
        self.listtree = listtree


class Poly(MaudeAttribute):
    def __init__(self, listtree):
        MaudeAttribute.__init__(self, AttributeType.poly)
        self.listtree = listtree


class Prec(MaudeAttribute):
    def __init__(self, tree):
        MaudeAttribute.__init__(self, AttributeType.prec)
        self.tree = tree


class Gather(MaudeAttribute):
    def __init__(self, listtree):
        MaudeAttribute.__init__(self, AttributeType.gather)
        self.listtree = listtree


class Format(MaudeAttribute):
    def __init__(self, listtree):
        MaudeAttribute.__init__(self, AttributeType.format)
        self.listtree = listtree


# System commands
class InCommand(AST):
    def __init__(self, filename):
        self.filename = filename

    def __eq__(self, other):
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

    def __eq__(self, other):
        return True


class EofCommand(AST):
    def commandtype(self):
        return CommandType.eofcommand

    def __eq__(self, other):
        return True


class PopDCommand(AST):
    def commandtype(self):
        return CommandType.popdcommand

    def __eq__(self, other):
        return True


class PwdCommand(AST):
    def commandtype(self):
        return CommandType.pwdcommand

    def __eq__(self, other):
        return True


class CdCommand(AST):
    def __init__(self, path):
        self.path = path

    def __eq__(self, other):
        return self.path == other.path

    def commandtype(self):
        return CommandType.cdcommand


class PushCommand(AST):
    def __init__(self, path):
        self.path = path

    def __eq__(self, other):
        return self.path == other.path

    def commandtype(self):
        return CommandType.pushcommand


class LsCommand(AST):
    def __init__(self, lsflags="", path=""):
        self.lsflags = lsflags
        self.path = path

    def __eq__(self, other):
        return self.path == other.path and self.lsflags == other.lsflags

    def commandtype(self):
        return CommandType.lscommand
