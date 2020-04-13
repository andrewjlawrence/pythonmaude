#ifndef TERM_H
#define TERM_H

#include <string>
#include <vector>
#include <iostream>
#include "variablename.hpp"
#include <boost/variant.hpp>

class VTerm;
class TTerm;

class Term {
public:
    Term();
    Term(const VTerm& vterm);
    Term(const TTerm& tterm); 
    ~Term();
    int which() const;
    const TTerm& asTTerm() const;
    const VTerm& asVTerm() const;
    Term& operator=(const TTerm& term);
    Term& operator=(const VTerm& term);
    friend std::ostream& operator<<(std::ostream& os, const Term& dt);
    bool operator==(const Term& other) const;
    std::string toString() const;
private:
    boost::variant<
      boost::recursive_wrapper<VTerm>,
      boost::recursive_wrapper<TTerm>
    > term;
};

using Term_t = Term;

enum TermType {
    VTerm_e = 0,
    TTerm_e = 1
};

using TermList_t = std::vector<Term_t>;

/**
 * Function to print the termlists
 */
std::ostream& operator<<(std::ostream& os, const TermList_t& terms);

#endif 