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


# Token
class Token(AST):
    def __init__(self, token):
        self.token = token

    def __eq__(self, other):
        return self.token == other.token

    def __repr__(self):
        return "<Token token: %s>" % (self.token)

    def __str__(self):
        return "From str method of Token: token is %s" % (self.token)


class TokenString(AST):
    def __init__(self, listtree):
        self.listtree = listtree

    def __eq__(self, other):
        return self.listtree == other.listtree

    def __repr__(self):
        return "<TokenString listtree: %s>" % (self.listtree)

    def __str__(self):
        return "From str method of TokenString: listtree is %s" % (self.listtree)


# Term
class Term(AST):
    def __init__(self, listtree):
        self.listtree = listtree

    def __eq__(self, other):
        return self.listtree == other.listtree

    def __repr__(self):
        return "<Term listtree: %s>" % (self.listtree)

    def __str__(self):
        return "From str method of Term: listtree is %s" % (self.listtree)

# Sort
class Sort(AST):
    def __init__(self, id, typelist):
        self.id = id
        self.typelist = typelist

    def __eq__(self, other):
        return self.id == other.id and self.typelist == other.typelist

    def __repr__(self):
        return "<Sort id: %s, typelist: %s>" % (self.id, self.typelist)

    def __str__(self):
        return "From str method of Sort: id is %s, typelist is %s" % (self.id, self.typelist)


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
        return Hook.__eq__(self, other) and self.name == other.name

    def __repr__(self):
        return "<IDHook name: %s, tree: %s>" % (self.name, self.tree)

    def __str__(self):
        return "From str method of IDHook: name is %s" % (self.name)


class OPHook(Hook):
    def __init__(self, tree):
        Hook.__init__(self, tree)

    def __eq__(self, other):
        return Hook.__eq__(self, other)

    def __repr__(self):
        return "<OPHook tree: %s>" % (self.tree)

    def __str__(self):
        return "From str method of OPHook: tree is %s" % (self.tree)


class TermHook(Hook):
    def __init__(self, tree):
        Hook.__init__(self, tree)

    def __eq__(self, other):
        return Hook.__eq__(self, other)

    def __repr__(self):
        return "<TermHook tree: %s>" % (self.tree)

    def __str__(self):
        return "From str method of TermHook: tree is %s" % (self.tree)


#
# Statement Attributes
#
class StatementAttributeType(Enum):
    nonexec = 1
    otherwise = 2
    variant = 3
    metadata = 4
    label = 5
    print = 6

class StatementAttribute(AST):
    def __init__(self, intype):
        self.attrtype = intype

    def __eq__(self, other):
        return self.attrtype == other.attrtype

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<StatementAttribute attrtype:%s>" % (self.attrtype.value)

    def __str__(self):
        return "From str method of StatementAttribute: attrtype is %s" % (self.attrtype.value)
#
# Attributes
#
class AttributeType(Enum):
    assoc = 1
    comm = 2
    id = 3
    idem = 4
    iter = 5
    memo = 6
    ditto = 7
    config = 8
    obj = 9
    msg = 10
    metadata = 11
    strat = 12
    poly = 13
    frozen = 14
    prec = 15
    gather = 16
    format = 17
    special = 18
    unknown = 19


class Attributes(AST):
    def __init__(self, attributelist):
        self.attributelist = attributelist

    def __eq__(self, other):
        if type(other) is type(self):
            return self.attributelist == other.attributelist
        return False


class IDDirection(Enum):
    left = 1
    right = 2
    none = 3


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


class ID(MaudeAttribute):
    def __init__(self, direction, tree):
        MaudeAttribute.__init__(self, AttributeType.id)
        self.direction = direction
        self.tree = tree

    def __eq__(self, other):
        return self.attrtype == other.attrtype and self.tree == other.tree

    def __repr__(self):
        return "<ID attrtype:%s, tree: %s>" % (self.attrtype.value, self.tree)

    def __str__(self):
        return "From str method of ID: attrtype is %s, tree is %s" % (self.attrtype.value, self.tree)


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
        return MaudeAttribute.__eq__(self, other) and any(i in self.listtree for i in other.listtree)

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
