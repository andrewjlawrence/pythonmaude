#ifndef SUBSTITUTION_H
#define SUBSTITUTION_H

#include <string>
#include <vector>
#include "term.hpp"

#if 0
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
#endif

/**
 *  A substitution 
 */
class Substitution
{
public:
    using Association_t = std::pair<VariableName, Term_t>;
    using AssociationList_t = std::vector<Association_t>;

    void addMapping(const VariableName& vname,
                    const Term_t& term);

    bool inDomain(const VariableName& vname) const;

private:
    AssociationList_t associationList;
};

#endif 