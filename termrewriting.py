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
        assert(type(name) == int)
        assert name
        self.name = name
        self.index = index


class TermType(Enum):
    VarTerm = 1
    TermList = 2


class Term(abc.ABC):
    @abstractmethod
    def occurs(self, vname : VName) -> bool:
        pass


# If this was C++ these would probably
# be in a single class with different constructors.
# Or some kind of union could be utilized.
class VTerm(Term):
    def __init__(self, vname : VName):
        assert(vname is VName)
        self.vname = vname
        self.type = TermType.VarTerm

    def occurs(self, vname :VName) -> bool:
        return self.vname == vname


class TTerm(Term):
    def __init__(self, term : str, termlist : List[Term]):
        assert(term is str)
        assert term
        assert(termlist is list)
        self.term = term
        self.termlist = termlist
        self.type = TermType.TermList

    def occurs(self, vname : VName) -> bool:
        return [x for x in list(map(lambda x: x.occurs(vname), self.termlist)) if x]

# Substituions are implemented as association lists
# of type (vname * term) list
class Substitution:
    def __init__(self):
        self._associationlist = list()

    def add_mapping(self, varname : VName, term : Term):
        assert(varname is VName)
        assert(term is VTerm or
               term is TTerm)
        self._associationlist.append((varname, term))

    def __getitem__(self, key : VName) -> Term:
        return self._associationlist[key]

    #  indom check if a variable is in the domain of a substitution
    def indom(self, varname : VName) -> bool:
        assert(varname is VName)
        return [x for (x,y) in self._associationlist if varname == x]

    def app(self, vterm : VTerm):
        for (var,term) in self._associationlist:
            if var == vterm.vname:
                return term
        return vterm

    def lift(self, term : Term) -> Term:
        assert(term is Term)
        if term is VTerm:
            return self.app(term)
        else:
            term.termlist = list(map(lambda terminlist: self.lift(terminlist), term.termlist))

class UnificationError(Exception):
    def __init__(self, message):
        self.message = message

def solve(termpairlist : List[Tuple[Term, Term]], subst : Substitution) -> Substitution:
    pass

def elim(vname : VName, term : Term, termpairlist : List[Tuple[Term, Term]], subst : Substitution) -> Substitution
    if term.occurs(vname):
        raise UnificationError("meh")
    else:
        xt = 

def unify(terma : Term, termb  : Term):
    solve([(terma, termb)], [])