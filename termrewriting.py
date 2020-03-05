#
# Python implementation of the examples from term rewriting and all that.
#
from enum import Enum


class VName:
    # A variable name is of type string * int
    def __init__(self, name, index):
        assert(type(name) == str)
        assert name
        self.name = name
        self.index = index


class TermType(Enum):
    VarTerm = 1
    TermList = 2

# If this was C++ these would probably
# be in a single class with different constructors.
# Or some kind of union could be utilized.
class VTerm:
    def __init__(self, vname):
        assert(type(vname) == VName)
        self.vname = vname
        self.type = TermType.VarTerm

class TTerm:
    def __init__(self, term, termlist):
        assert(type(term) == str)
        assert term
        assert(type(termlist) == list)
        self.term = term
        self.termlist = termlist
        self.type = TermType.TermList

# Substituions are implemented as association lists
# of type (vname * term) list
class Substitution:
    def __init__(self):
        self._associationlist = list()

    def add_mapping(self, varname, term):
        assert(type(varname) == VName)
        assert(type(term) == VTerm or
               type(term) == TTerm)
        self._associationlist.append((varname, term))

    def __getitem__(self, key):
        return self._associationlist[key]



