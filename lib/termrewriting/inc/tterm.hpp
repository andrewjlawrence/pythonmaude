#ifndef TTERM_H
#define TTERM_H

#include "term.hpp"

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

    std::string toString() const;
    
private:
    std::string term;
    TermList_t subterms;
};

#endif 