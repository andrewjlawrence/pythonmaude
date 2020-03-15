#
# Python implementation of the examples from term rewriting and all that.
#
from enum import Enum
from typing import List, Tuple
import abc

class VName:
    # A variable name is of type string * int
    def __init__(self, name : str, index : int):
        assert(type(name) == str)
        assert(type(index) == int)
        assert name
        self.name = name
        self.index = index

    def __eq__(self, other):
        if not isinstance(other, VName):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.name == other.name and self.index == other.index

class TermType(Enum):
    VarTerm = 1
    TermList = 2


class Term(abc.ABC):
    @abc.abstractmethod
    def occurs(self, vname : VName) -> bool:
        pass


# If this was C++ these would probably
# be in a single class with different constructors.
# Or some kind of union could be utilized.
class VTerm(Term):
    def __init__(self, vname : VName):
        assert(type(vname) == VName)
        self.vname = vname
        self.type = TermType.VarTerm

    def occurs(self, vname :VName) -> bool:
        return self.vname == vname

    def __str__(self):
        return "<termrewriting.VTerm vname : {0}, type : {1}>".format(self.vname, self.type)


class TTerm(Term):
    def __init__(self, term : str, termlist : List[Term]):
        assert(type(term) == str)
        assert term
        assert(type(termlist) is list)
        self.term = term
        self.termlist = termlist
        self.type = TermType.TermList

    def occurs(self, vname : VName) -> bool:
        return [x for x in list(map(lambda x: x.occurs(vname), self.termlist)) if x]

    def __str__(self):
        return "<termrewriting.TTerm vname : {0}, type : {1}, termlist : {2}>".format(self.vname, self.type, self.termlist)

    def __repr__(self):
        return "<termrewriting.TTerm vname : {0}, type : {1}, termlist : {2}>".format(self.vname, self.type, self.termlist)

# Substituions are implemented as association lists
# of type (vname * term) list
class Substitution:
    def __init__(self):
        self._associationlist = list()

    def add_mapping(self, varname : VName, term : Term):
        assert(type(varname) == VName)
        assert(type(term) == VTerm or
               type(term) == TTerm)
        self._associationlist.append((varname, term))

    def __getitem__(self, key : VName) -> Term:
        return self._associationlist[key]

    #  indom check if a variable is in the domain of a substitution
    def indom(self, varname : VName) -> bool:
        assert(type(varname) == VName)
        return [x for (x,y) in self._associationlist if varname == x]

    # Apply the substitution to a variable term
    def app(self, vterm : VTerm):
        for (var,term) in self._associationlist:
            if var == vterm.vname:
                return term
        return vterm

    # Lift a term and apply the subsitution to
    # all of the subterms
    def lift(self, term : Term) -> Term:
        assert(issubclass(type(term), Term))
        if type(term) == VTerm:
            return self.app(term)
        else:
            term.termlist = list(map(lambda terminlist: self.lift(terminlist), term.termlist))
            return term

class UnificationError(Exception):
    def __init__(self, message):
        self.message = message



def solve(termpairlist : List[Tuple[Term, Term]], subst : Substitution) -> Substitution:
    if not termpairlist:
        return subst
    elif termpairlist[0][0] is VTerm:
        if termpairlist[0][0] == termpairlist[0][1]:
            return solve(termpairlist[1:], subst)
        else:
            return elim(termpairlist[0][0],termpairlist[0][1], termpairlist[1:], subst)
    elif termpairlist[0][1] is VTerm:
        return elim(termpairlist[0][1],termpairlist[0][0], termpairlist[1:], subst)
    else:
        assert termpairlist[0][0] is TTerm
        assert termpairlist[0][1] is TTerm
        if termpairlist[0][0].term == termpairlist[0][1].term:
            solve(zip(termpairlist[0][0].termlist, termpairlist[0][1].termlist) + termpairlist[1:])
        else:
            raise UnificationError("meh")


def elim(vname : VName, term : Term, termpairlist : List[Tuple[Term, Term]], subst : Substitution) -> Substitution:
    if term.occurs(vname):
        raise UnificationError("meh")
    else:
        xtsubst = Substitution()
        xtsubst.add_mapping(vname,term)
        liftedlist = list(map(lambda termpair: (xtsubst.lift(termpair[0]), xtsubst.lift(termpair[1])), termpairlist))
        solve(liftedlist, [(vname, term)] + list(map(lambda pair: (pair[0], xtsubst.lift(pair[1])), subst)))


def unify(terma : Term, termb: Term):
    solve([(terma, termb)], [])