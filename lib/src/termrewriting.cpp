
#include "termrewriting.hpp"

Substitution TermRewriting::matchs(const AssociationList_t& associationList,
                                   const Substitution& substitution)
{
    if (!associationList.empty())
    {
        if(associationList[0].first)
    }
    else
    {
        return substitution;
    }
}

Substitution match(const Term_t& pat, const Term_t& obj)
{

}


#if 0
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
#endif