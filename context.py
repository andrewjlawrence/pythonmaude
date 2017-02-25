from ast import Op,Sort,Ident,EqStatement

class Context:
    def __init__(self):
        self.sorts = set()
        self.ops = set()
        self.eqs = set()
        self.vars = set()

    def addOp(self, op:Op):
        self.ops.add(op)

    def addSort(self, sort:Sort):
        self.sort.add(sort)

    def addVar(self, var:Ident):
        self.vars.add(var)

    def addEq(self, eq:EqStatement):
        self.eqs.add(eq)