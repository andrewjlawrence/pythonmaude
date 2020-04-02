#ifndef TERM_H
#define TERM_H

#include <string>
#include <vector>
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
private:
    VariableName varname;
};

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
private:
    std::string term;
    TermList_t subterms;
};

#endif 