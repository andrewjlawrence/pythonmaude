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

using Association_t = std::pair<VariableName, Term_t>;
using AssociationList_t = std::vector<Association_t>;

/**
 *  A substitution maps a bunch of variables to some terms.
 */
class Substitution
{
public:
    /**
     * Add a mapping to the substitution
     * @param vname The variable name to use on the left handside of the mapping.
     * @param term The term that the variable has been substituted with.
     */
    void addMapping(const VariableName& vname,
                    const Term_t& term);

    /**
     * Check whether a variable name is in the domain of the substitution.
     * @param vname The variable name that we will check for
     * @return true if the variable name is domain (left hand side) of the mapping 
     *         false otherwise.
     */ 
    bool inDomain(const VariableName& vname) const;

    /**
     * Apply the substitution to a term with a variable to get a new term
     * @param vterm The term to which the substitution will be applied
     * @result The term resulting from apply the substitution to vterm.
     */
    const Term_t app(const VTerm& vterm) const;

    /**
     * Lift a term
     * Both this method and the above are making copies and could be
     * refactored to be faster.
     */
    const Term_t lift(const Term_t& vterm) const;

    /**
     * Friend output stream operator to print substitutions
     */
    friend std::ostream& operator<<(std::ostream& os, const Substitution& dt);
private:
    AssociationList_t associationList;
};

#endif 