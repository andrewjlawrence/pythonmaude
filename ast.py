# Copyright 2017 Andrew Lawrence
from enum import Enum
from functools import reduce
from exceptions import MaudeException

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
    def __init__(self, lineno=0, colno=0):
        self.lineno = lineno
        self.colno = colno



# Identifier
class Ident(AST):
    def __init__(self, name, lineno, colno):
        AST.__init__(self, lineno, colno)
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<Ident name:%s lineno:%s colno:%s>" % (self.name,
                                                       self.lineno,
                                                       self.colno)

    def __str__(self):
        return "From str method of Ident: name is %s, lineno is %s, colno is %s" % (self.name,
                                                                                    self.lineno,
                                                                                    self.colno)

    def __hash__(self):
        return hash(self.name)


# Literal
class Literal(AST):
    def __init__(self, value):
        self.value = value


# Token
class Label(AST):
    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "<Label id: %s>" % (self.id)

    def __str__(self):
        return "From str method of ID: id is %s" % (self.id)


# Token
class Token(AST):
    def __init__(self, token):
        self.token = token

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "<Token token: %s>" % (self.token)

    def __str__(self):
        return "From str method of Token: token is %s" % (self.token)


class TokenString(AST):
    def __init__(self, listtree):
        self.listtree = listtree

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "<TokenString listtree: %s>" % (self.listtree)

    def __str__(self):
        return "From str method of TokenString: listtree is %s" % (self.listtree)


# Term
class Term(AST):
    def __init__(self, listtree):
        self.listtree = listtree

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

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
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<Sort id: %s, typelist: %s>" % (self.id, self.typelist)

    def __str__(self):
        return "From str method of Sort: id is %s, typelist is %s" % (self.id, self.typelist)

    def __hash__(self):
        listhash = 0
        for x in self.typelist:
            listhash ^ hash(self.typelist)
        return hash(self.id) ^ listhash


# Subsort
class Subsort(AST):
    def __init__(self, subsort, sortlist):
        self.subsort = subsort
        self.sortlist = sortlist

    def __eq__(self, other):
        return self.subsort == other.subsort and any(i in self.sortlist for i in other.sortlist)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<Subsort subsort: %s, sortlist: %s>" % (self.subsort, self.sortlist)

    def __str__(self):
        return "From str method of Subsort: subsort is %s, sortlist is %s" % (self.subsort, self.sortlist)


# Hooks
class Hook(AST):
    def __init__(self, tree):
        self.tree = tree

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

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
# Conditions
#
class Condition(AST):
    def __init__(self, fragmentlist):
        self.fragmentlist = fragmentlist

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<Condition fragmentlist:%s>" % (self.fragmentlist)

    def __str__(self):
        return "From str method of Condition: fragmentlist is %s" % (self.fragmentlist)


class EqFragment(AST):
    def __init__(self, leftterm: Term, rightterm: Term):
        self.leftterm = leftterm
        self.rightterm = rightterm

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<EQFragment leftterm:%s , rightterm:%s>" % (self.leftterm, self.rightterm)

    def __str__(self):
        return "From str method of EQFragment: leftterm is %s, rightterm is %s" % (self.leftterm, self.rightterm)


class AssigmentFragment(AST):
    def __init__(self, leftterm: Term, rightterm: Term):
        self.leftterm = leftterm
        self.rightterm = rightterm

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<AssigmentFragment leftterm:%s , rightterm:%s>" % (self.leftterm, self.rightterm)

    def __str__(self):
        return "From str method of AssigmentFragment: leftterm is %s, rightterm is %s" % (self.leftterm, self.rightterm)


class SubsortFragment(AST):
    def __init__(self, term: Term, sort: Sort):
        self.term = term
        self.sort = sort

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<SubsortFragment term:%s , sort:%s>" % (self.term, self.sort)

    def __str__(self):
        return "From str method of SubsortFragment: term is %s, sort is %s" % (self.term, self.sort)


#
# Statements
#
class Equation(AST):
    def __init__(self, leftterm: Term, rightterm: Term):
        self.leftterm = leftterm
        self.rightterm = rightterm

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<EqStatement leftterm:%s, rightterm:%s>" % (self.leftterm, self.rightterm)

    def __str__(self):
        return "From str method of EqStatement: leftterm is %s, rightterm is %s" % (self.leftterm, self.rightterm)


class ConditionalEquation(AST):
    def __init__(self, leftterm: Term, rightterm: Term, condition: Condition):
        self.leftterm = leftterm
        self.rightterm = rightterm
        self.condition = condition

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<CeqStatement leftterm:%s, rightterm:%s, condition:%s>" % (self.leftterm, self.rightterm, self.condition)

    def __str__(self):
        return "From str method of CeqStatement: leftterm is %s, rightterm is %s, condition is %s" % \
               (self.leftterm, self.rightterm, self.condition)


class MbStatement(AST):
    def __init__(self, term: Term, sort: Sort):
        self.term = term
        self.sort = sort

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<MbStatement term:%s, sort:%s>" % (self.term, self.sort)

    def __str__(self):
        return "From str method of MbStatement: term is %s, sort is %s" % (self.term, self.sort)


class CmbStatement(AST):
    def __init__(self, term: Term, sort: Sort, condition: Condition):
        self.term = term
        self.sort = sort
        self.condition = condition

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<CeqStatement term:%s, sort:%s, condition:%s>" % (self.term, self.sort, self.condition)

    def __str__(self):
        return "From str method of CeqStatement: term is %s,\nsort is %s,\ncondition is %s" % \
               (self.term, self.sort, self.condition)


class RlStatement(AST):
    def __init__(self, leftterm: Term, rightterm: Term):
        self.leftterm = leftterm
        self.rightterm = rightterm

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<RlStatement leftterm:%s, rightterm:%s>" % (self.leftterm, self.rightterm)

    def __str__(self):
        return "From str method of RlStatement: leftterm is %s, rightterm is %s" % (self.leftterm, self.rightterm)

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
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<StatementAttribute attrtype:%s>" % (self.attrtype.value)

    def __str__(self):
        return "From str method of StatementAttribute: attrtype is %s" % (self.attrtype.value)

#
# Module elements
#
class Include(AST):
    def __init__(self, modexp):
        self.modexp = modexp

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<Include modexp:%s>" % (self.modexp)

    def __str__(self):
        return "From str method of Include: modexp is %s" % (self.modexp)


class Extend(AST):
    def __init__(self, modexp):
        self.modexp = modexp

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<Extend modexp:%s>" % (self.modexp)

    def __str__(self):
        return "From str method of Extend: modexp is %s" % (self.modexp)


class Protect(AST):
    def __init__(self, modexp):
        self.modexp = modexp

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<Protect modexp:%s>" % (self.modexp)

    def __str__(self):
        return "From str method of Protect: modexp is %s" % (self.modexp)


class Sorts(AST):
    def __init__(self, sortlist):
        self.sortlist = sortlist

    def __eq__(self, other):
        return self.sortlist == other.sortlist

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<Sorts sortlist:%s>" % (self.sortlist)

    def __str__(self):
        return "From str method of Sorts: sortlist is %s" % (self.sortlist)


class Op(AST):
    def __init__(self, opform, insortlist, arrow, outsort : Sort, attrs):
        self.opform = opform
        self.insortlist = insortlist
        self.arrow = arrow
        self.outsort = outsort
        self.attrs = attrs
        self.parser = self.opformtoparser()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<Op opform:%s insortlist:%s arrow:%s outsort:%s attrs:%s>" % (self.opform,
                                                                              self.insortlist,
                                                                              self.arrow,
                                                                              self.outsort,
                                                                              self.attrs)

    def __str__(self):
        return "From str method of Op: opform is %s, insortlist is %s, arrow is %s, outsort is %s, attrs is %s" % (self.opform,
                                                                                                                   self.insortlist,
                                                                                                                   self.arrow,
                                                                                                                   self.outsort,
                                                                                                                   self.attrs)

    def getsorts(self):
        outlist = self.insortlist
        outlist.append(self.outsort)
        return outlist

    def opformtoparser(self):
        pass


class Vars(AST):
    def __init__(self, varlist, maudetype):
        self.varlist = list()
        for var in varlist:
            self.varlist.append(Var(var, maudetype))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<Vars varlist:%s>" % (self.varlist)

    def __str__(self):
        return "From str method of Vars: varlist is %s" % (self.varlist)


class Var(AST):
    def __init__(self, id, maudetype):
        self.id = id
        self.maudetype = maudetype

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def getsort(self):
        return self.maudetype.id

    def __repr__(self):
        return "<Var id:%s, maudetype:%s>" % (self.id, self.maudetype)

    def __str__(self):
        return "From str method of Vars: varlist is %s" % (self.varlist)



class Statement(AST):
    def __init__(self, statement, attributes):
        self.statement = statement
        self.attributes = attributes

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<Statement statement:%s attributes:%s>" % (self.statement, self.attributes)

    def __str__(self):
        return "From str method of Statement: statement is %s, attributes is %s" % (self.statement, self.attributes)
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
        return self.__dict__ == other.__dict__

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
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "<ID attrtype:%s, tree: %s>" % (self.attrtype.value, self.tree)

    def __str__(self):
        return "From str method of ID: attrtype is %s, tree is %s" % (self.attrtype.value, self.tree)


class MetaData(MaudeAttribute):
    def __init__(self, tree):
        MaudeAttribute.__init__(self, AttributeType.metadata)
        self.tree = tree

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "<MetaData attrtype:%s, tree: %s>" % (self.attrtype.value, self.tree)

    def __str__(self):
        return "From str method of MetaData: attrtype is %s" % (self.attrtype.value)


class Strat(MaudeAttribute):
    def __init__(self, listtree):
        MaudeAttribute.__init__(self, AttributeType.strat)
        self.listtree = listtree

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "<Strat attrtype:%s, listtree: %s>" % (self.attrtype.value, self.listtree)

    def __str__(self):
        return "From str method of Strat: attrtype is %s" % (self.attrtype.value)


class Poly(MaudeAttribute):
    def __init__(self, listtree):
        MaudeAttribute.__init__(self, AttributeType.poly)
        self.listtree = listtree

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

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
        return self.__dict__ == other.__dict__


class Gather(MaudeAttribute):
    def __init__(self, listtree):
        MaudeAttribute.__init__(self, AttributeType.gather)
        self.listtree = listtree

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Format(MaudeAttribute):
    def __init__(self, listtree):
        MaudeAttribute.__init__(self, AttributeType.format)
        self.listtree = listtree

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Special(MaudeAttribute):
    def __init__(self, listtree):
        MaudeAttribute.__init__(self, AttributeType.special)
        self.listtree = listtree

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "<Special attrtype:%s, listtree: %s>" % (self.attrtype.value, self.listtree)

    def __str__(self):
        return "From str method of Special: attrtype is %s" % (self.attrtype.value)


# Modules
class Module(AST):
    def __init__(self, moduleid, parameterlist):
        self.moduleid = moduleid
        self.parameterlist = parameterlist
        self.sorts = dict()
        self.ops = set()
        self.eqs = set()
        self.vars = set()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "<Module module:%s parameterlist:%s sorts:%s>" % (self.moduleid,
                                                                 self.parameterlist,
                                                                 self.sorts,
                                                                 self.ops,
                                                                 self.eqs,
                                                                 self.vars)

    def __str__(self):
        return "From str method of Module: module is %s, parameterlist is %s, elementlist is %s" % (self.moduleid,
                                                                                                    self.parameterlist,
                                                                                                    self.elementlist,
                                                                                                    self.sorts,
                                                                                                    self.ops,
                                                                                                    self.vars)

    def addop(self, op: Op):
        for sort in op.getsorts():
            if sort in self.sorts:
                self.ops.add(op)
            else:
                raise MaudeException("Unknown sort: %s" % sort)

    def addsort(self, sort: Sort):
        self.sorts[sort.id] = sort.typelist

    def addvar(self, var: Var):
        if var.getsort() in self.sorts:
            self.vars.add(var)
        else:
            raise MaudeException("Unknown sort: %s" % var.getsort())

    def addeq(self, eq: Equation):
        self.eqs.add(eq)



# System commands
class InCommand(AST):
    def __init__(self, filename):
        self.filename = filename

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def commandtype(self):
        return CommandType.incommand


class LoadCommand(AST):
    def __init__(self, filename):
        self.filename = filename

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

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
        return self.__dict__ == other.__dict__

    def commandtype(self):
        return CommandType.cdcommand


class PushCommand(AST):
    def __init__(self, path):
        self.path = path

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def commandtype(self):
        return CommandType.pushcommand


class LsCommand(AST):
    def __init__(self, lsflags="", path=""):
        self.lsflags = lsflags
        self.path = path

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def commandtype(self):
        return CommandType.lscommand
