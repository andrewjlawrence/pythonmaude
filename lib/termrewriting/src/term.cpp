#include "term.hpp"
#include "tterm.hpp"
#include "vterm.hpp"
#include <algorithm>
#include <sstream>


Term::Term()
:term(VTerm(VariableName()))
{
}

Term::Term(const VTerm& vterm)
:term(vterm)
{
}
    
Term::Term(const TTerm& tterm)
:term(tterm)
{
}

Term::~Term()
{
}
    
int Term::which() const
{
    return term.which();
}
    
const TTerm& Term::asTTerm() const
{
    return boost::get<TTerm>(term);
}
    
const VTerm& Term::asVTerm() const
{
    return boost::get<VTerm>(term);
}
   
Term& Term::operator=(const TTerm& term)
{
    this->term = term;
    return *this;
}
    
Term& Term::operator=(const VTerm& term)
{
    this->term = term;
    return *this;
}
    
std::ostream& operator<<(std::ostream& os, const Term& dt)
{
    return os << dt.toString();
}

bool Term::operator==(const Term& other) const
{
    return this->term == other.term;
}

std::string Term::toString() const
{
    if (term.which() == TTerm_e)
    {
        return asTTerm().toString();
    }
    else
    {
        // For now this is the only aternative
        return asVTerm().toString();
    }
}

std::ostream& operator<<(std::ostream& os, const TermList_t& terms)
{
    os << "[ ";
    for (int i = 0; i < terms.size(); i++)
    {
        os << terms[i];
        if (i+1 != terms.size())
        {
            os << ", ";
        }
    }
    os << "]";
    return os;
}
