# Copyright 2017 Andrew Lawrence

from ast import Op,Sort,Var,Equation
from exceptions import MaudeException


class Context:
    def __init__(self):
        self.sorts = dict()
        self.ops = set()
        self.eqs = set()
        self.vars = set()

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

