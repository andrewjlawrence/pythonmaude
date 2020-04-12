#ifndef SUBSTITUTION_H
#define SUBSTITUTION_H

#include <string>
#include <vector>
#include "term.hpp"

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