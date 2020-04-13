#ifndef VTERM_H
#define VTERM_H

#include "variablename.hpp"

/**
 * Class to store a term that consists solely of a variable
 */
class VTerm
{
public:
    VTerm(const VariableName& variableName);
    const VariableName& getVariableName() const;
    bool occurs(const VariableName& vname) const;

    /**
     * Comparison operator
     */
    bool operator==(const VTerm& other) const;

    /**
     * Friend output stream operator to print VTerms
     */
    friend std::ostream& operator<<(std::ostream& os, const VTerm& dt);

    /**
     * Convert the object to a string.
     */
    const std::string toString() const;
private:
    VariableName varname;
};

#endif