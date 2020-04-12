#ifndef TERM_H
#define TERM_H

#include <string>
#include <vector>
#include <iostream>
#include "variablename.hpp"
#include <boost/variant.hpp>

class VTerm;
class TTerm;

using Term_t = boost::variant<
      boost::recursive_wrapper<VTerm>,
      boost::recursive_wrapper<TTerm>
    >;

enum TermType {
    VTerm_e = 0,
    TTerm_e = 1
};

using TermList_t = std::vector<Term_t>;

/**
 * Function to print the termlists
 */
std::ostream& operator<<(std::ostream& os, const TermList_t& terms);

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

/**
 * Class to store nary terms
 */
class TTerm
{
public:
    TTerm(const std::string& termname,
          const TermList_t& subterms);

    const std::string& getTerm() const;
    const std::vector<Term_t>&  getSubterms() const;
    Term_t& operator[](size_t index);
    const Term_t& operator[](size_t index) const;

    bool occurs(const VariableName& vname) const;

    /**
     * Comparison operator
     */
    bool operator==(const TTerm& other) const;

    friend std::ostream& operator<<(std::ostream& os, const TTerm& dt);
private:
    std::string term;
    TermList_t subterms;
};

#endif 