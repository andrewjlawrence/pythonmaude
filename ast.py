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

# Hooks
class Hook(AST):
    def __init__(self, tree):
        self.tree = tree

    def __eq__(self, other):
        return self.tree == other.tree

    def __repr__(self):
        return "<Hook tree: %s>" % (self.tree)

    def __str__(self):
        return "From str method of Hook: tree is %s" % (self.tree)


class IDHook(Hook):
    def __init__(self, name, tree):
        self.name = name
        Hook.__init__(self, tree)

    def __eq__(self, other):
        return Hook.__eq__(self,other) and self.name == other.name

    def __repr__(self):
        return "<IDHook name: %s, tree: %s>" % (self.name, self.tree)

    def __str__(self):
        return "From str method of IDHook: name is %s" % (self.name)


class OPHook(Hook):
    def __init__(self, tree):
        Hook.__init__(self, tree)

    def __eq__(self, other):
        return Hook.__eq__(self,other)

    def __repr__(self):
        return "<OPHook tree: %s>" % (self.tree)

    def __str__(self):
        return "From str method of OPHook: tree is %s" % (self.tree)


class TermHook(Hook):
    def __init__(self, tree):
        Hook.__init__(self, tree)

    def __eq__(self, other):
        return Hook.__eq__(self,other)

    def __repr__(self):
        return "<TermHook tree: %s>" % (self.tree)

    def __str__(self):
        return "From str method of TermHook: tree is %s" % (self.tree)


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
            return self.attributelist == other.attributelist
        return False


class MaudeAttribute(AST):
    def __init__(self, intype):
        self.attrtype = intype

    def __eq__(self, other):
        return self.attrtype == other.attrtype

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<MaudeAttribute attrtype:%s>" % (self.attrtype.value)

    def __str__(self):
        return "From str method of MaudeAttribute: attrtype is %s" % (self.attrtype.value)


class LeftID(MaudeAttribute):
    def __init__(self, tree):
        MaudeAttribute.__init__(self, AttributeType.left)
        self.tree = tree

    def __eq__(self, other):
        return self.attrtype == other.attrtype and self.tree == other.tree

    def __repr__(self):
        return "<LeftID attrtype:%s, tree: %s>" % (self.attrtype.value, self.tree)

    def __str__(self):
        return "From str method of LeftID: attrtype is %s" % (self.attrtype.value)


class RightID(MaudeAttribute):
    def __init__(self, tree):
        MaudeAttribute.__init__(self, AttributeType.right)
        self.tree = tree

    def __eq__(self, other):
        return self.attrtype == other.attrtype and self.tree == other.tree

    def __repr__(self):
        return "<RightID attrtype:%s, tree: %s>" % (self.attrtype.value, self.tree)

    def __str__(self):
        return "From str method of RightID: attrtype is %s" % (self.attrtype.value)


class MetaData(MaudeAttribute):
    def __init__(self, tree):
        MaudeAttribute.__init__(self, AttributeType.metadata)
        self.tree = tree

    def __eq__(self, other):
        return self.attrtype == other.attrtype and self.tree == other.tree

    def __repr__(self):
        return "<MetaData attrtype:%s, tree: %s>" % (self.attrtype.value, self.tree)

    def __str__(self):
        return "From str method of MetaData: attrtype is %s" % (self.attrtype.value)


class Strat(MaudeAttribute):
    def __init__(self, listtree):
        MaudeAttribute.__init__(self, AttributeType.strat)
        self.listtree = listtree

    def __eq__(self, other):
        return self.attrtype == other.attrtype and self.listtree == other.listtree

    def __repr__(self):
        return "<Strat attrtype:%s, listtree: %s>" % (self.attrtype.value, self.listtree)

    def __str__(self):
        return "From str method of Strat: attrtype is %s" % (self.attrtype.value)


class Poly(MaudeAttribute):
    def __init__(self, listtree):
        MaudeAttribute.__init__(self, AttributeType.poly)
        self.listtree = listtree

    def __eq__(self, other):
        return self.attrtype == other.attrtype and self.listtree == other.listtree

    def __repr__(self):
        return "<Poly attrtype:%s, listtree: %s>" % (self.attrtype.value, self.listtree)

    def __str__(self):
        return "From str method of Poly: attrtype is %s" % (self.attrtype.value)


class Frozen(MaudeAttribute):
    def __init__(self, listtree):
        MaudeAttribute.__init__(self, AttributeType.frozen)
        self.listtree = listtree

    def __eq__(self, other):
        return MaudeAttribute.__eq__(self,other) and any(i in self.listtree for i in other.listtree)

    def __ne__(self, other):
        return not self.__eq__(self, other)

    def __repr__(self):
        return "<Frozen attrtype:%s, listtree: %s>" % (self.attrtype.value, self.listtree)

    def __str__(self):
        return "From str method of Frozen: attrtype is %s" % (self.attrtype.value)


class Prec(MaudeAttribute):
    def __init__(self, tree):
        MaudeAttribute.__init__(self, AttributeType.prec)
        self.tree = tree

    def __eq__(self, other):
        return self.attrtype == other.attrtype and self.tree == other.tree


class Gather(MaudeAttribute):
    def __init__(self, listtree):
        MaudeAttribute.__init__(self, AttributeType.gather)
        self.listtree = listtree

    def __eq__(self, other):
        return self.attrtype == other.attrtype and self.listtree == other.listtree


class Format(MaudeAttribute):
    def __init__(self, listtree):
        MaudeAttribute.__init__(self, AttributeType.format)
        self.listtree = listtree

    def __eq__(self, other):
        return self.attrtype == other.attrtype and self.listtree == other.listtree


class Special(MaudeAttribute):
    def __init__(self, listtree):
        MaudeAttribute.__init__(self, AttributeType.special)
        self.listtree = listtree

    def __eq__(self, other):
        return self.attrtype == other.attrtype and self.listtree == other.listtree

    def __repr__(self):
        return "<Special attrtype:%s, listtree: %s>" % (self.attrtype.value, self.listtree)

    def __str__(self):
        return "From str method of Special: attrtype is %s" % (self.attrtype.value)

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
