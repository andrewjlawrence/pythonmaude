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

    def __key(self):
        return (self.name, self.index)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if not isinstance(other, VName):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.__key() == other.__key()

    def __str__(self):
        return "<VName name : {0} , index : {1} >".format(self.name, self.index)

    def __repr__(self):
        return "<VName name : {0} , index : {1} >".format(self.name, self.index)

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
        return "<VTerm vname : {0}, type : {1}>".format(self.vname, self.type)

    def __repr__(self):
        return "<VTerm vname : {0}, type : {1}>".format(self.vname, self.type)

    def __key(self):
        return (self.vname, self.type)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if not isinstance(other, VTerm):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.__key() == other.__key()


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
        return "<TTerm vname : {0}, type : {1}, termlist : {2}>".format(self.term, self.type, self.termlist)

    def __repr__(self):
        return "<TTerm vname : {0}, type : {1}, termlist : {2}>".format(self.term, self.type, self.termlist)

    def __key(self):
        return (self.term, tuple(self.termlist), self.type)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if not isinstance(other, TTerm):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.__key() == other.__key()


# Substituions are implemented as association lists
# of type (vname * term) list
class Substitution:
    def __init__(self, asso_list=None):
        if asso_list is None:
            asso_list = []
        self._associationlist = asso_list

    def __getitem__(self, key : VName) -> Term:
        return self._associationlist[key]

    def __len__(self):
        return len(self._associationlist)

    def __str__(self):
        return "<Substitutuon associationlist : {0} >".format(self._associationlist)

    def __repr__(self):
        return "<Substitutuon associationlist : {0} >".format(self._associationlist)

    def add_mapping(self, varname : VName, term : Term):
        assert(type(varname) == VName)
        assert(type(term) == VTerm or
               type(term) == TTerm)
        if not (varname, term) in self._associationlist:
            self._associationlist.append((varname, term))

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
        #assert(issubclass(type(term), Term))
        if type(term) == VTerm:
            return self.app(term)
        else:
            term.termlist = list(map(lambda terminlist: self.lift(terminlist), term.termlist))
            return term

class UnificationError(Exception):
    def __init__(self, message):
        self.message = message

def uniqueappend(list1, list2):
    for ele in list2:
        if not ele in list1:
            list1.append(ele)
    return list1

#
# This is the syntactic unification based on chapter 2.5 of term rewriting and all that.
#
def solve(termpairlist : List[Tuple[Term, Term]], subst : Substitution) -> Substitution:
    if not termpairlist:
        return subst
    elif type(termpairlist[0][0]) == VTerm:
        if termpairlist[0][0] == termpairlist[0][1]:
            return solve(termpairlist[1:], subst)
        else:
            return elim(termpairlist[0][0],termpairlist[0][1], termpairlist[1:], subst)
    elif type(termpairlist[0][1]) == VTerm:
        return elim(termpairlist[0][1],termpairlist[0][0], termpairlist[1:], subst)
    else:
        assert type(termpairlist[0][0]) == TTerm
        assert type(termpairlist[0][1]) == TTerm
        if termpairlist[0][0].term == termpairlist[0][1].term:
            return solve(list(zip(termpairlist[0][0].termlist, termpairlist[0][1].termlist)) + termpairlist[1:], subst)
        else:
            raise UnificationError("meh")

def elim(vterm : VTerm, term : Term, termpairlist : List[Tuple[Term, Term]], subst : Substitution) -> Substitution:
    if term.occurs(vterm.vname):
        raise UnificationError("meh")
    else:
        xtsubst = Substitution()
        xtsubst.add_mapping(vterm.vname,term)
        liftedlist = list(map(lambda termpair: (xtsubst.lift(termpair[0]), xtsubst.lift(termpair[1])), termpairlist))
        return solve(liftedlist, Substitution(uniqueappend([(vterm.vname, term)], list(map(lambda pair: (pair[0], xtsubst.lift(pair[1])), subst)))))


def unify(terma : Term, termb: Term) -> Substitution:
    return solve([(terma, termb)],  Substitution())


#
# The following algorithm is a special case of unificTION
#
def matchs(termpairlist : List[Tuple[Term, Term]],  subst : Substitution) -> Substitution:
    if not termpairlist:
        return subst
    elif type(termpairlist[0][0]) == VTerm:
        if subst.indom(termpairlist[0][0].vname):
            if subst.apply(termpairlist[0][0].vname) == termpairlist[0][1]:
                return matchs(termpairlist[1:], subst)
            else:
                raise UnificationError("meh")
        else:
            subst.add_mapping(termpairlist[0][0].vname, termpairlist[0][1])
            return matchs(termpairlist[1:], subst)
    elif type(termpairlist[0][1]) == VTerm:
        raise UnificationError("meh")
    else:
        assert type(termpairlist[0][0]) == TTerm
        assert type(termpairlist[0][1]) == TTerm
        if termpairlist[0][0].term == termpairlist[0][1].term:
            return matchs(list(zip(termpairlist[0][0].termlist, termpairlist[0][1].termlist)) + termpairlist[1:], subst)
        else:
            raise UnificationError("meh")

class NormalizationError(Exception):
    def __init__(self, message):
        self.message = message


def match(pat : Term, obj : Term) -> Substitution:
    return matchs([(pat, obj)], Substitution())


def rewrite(termlist : List[Tuple[Term, Term]], term : Term) -> Term:
    if termlist:
        try:
            return match(termlist[0][0], term).lift(termlist[0][1])
        except UnificationError:
            return rewrite(termlist[1:], term)
    else:
        raise NormalizationError("meh")


def normalize(termlist, term):
    if type(term) == VTerm:
        return term
    else:
        newlist = list()
        for termtonormalize in term.termlist:
            newlist.append(normalize(termlist,termtonormalize))
        term.termlist = newlist
        try:
            return normalize(termlist, rewrite(termlist, term))
        except NormalizationError:
            return term



