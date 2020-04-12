#include "term.hpp"
#include <algorithm>

VTerm::VTerm(const VariableName& variableName)
:varname(variableName)
{
}

const VariableName& VTerm::getVariableName() const
{
    return varname;
}
    
bool VTerm::occurs(const VariableName& vname) const
{
    return varname == vname;
}


TTerm::TTerm(const std::string& termname,
             const TermList_t& subterms)
:term(termname), subterms(subterms)
{
}

const std::string& TTerm::getTerm() const
{
    return term;
}

const std::vector<Term_t>&  TTerm::getSubterms() const
{
    return subterms;
}

bool TTerm::occurs(const VariableName& vname) const
{
    return std::any_of(subterms.cbegin(),
                       subterms.cend(),
        [&vname](const Term_t& x){
            bool result(false);
            switch (x.which()) {
                case VTerm_e: 
                    result = boost::get<VTerm>(x).occurs(vname);
                    break;
                case TTerm_e: 
                    result = boost::get<TTerm>(x).occurs(vname);
                    break;
                default:
                    result = false;
                    break;
            }
            return result;
        }
    );
}

Term_t& TTerm::operator[](size_t index)
{
    return subterms[index];
}
    
const Term_t& TTerm::operator[](size_t index) const
{
    return subterms[index];
}

bool TTerm::operator==(const TTerm& other) const
{
    return this->term == other.term && this->subterms == other.subterms;
}

std::ostream& operator<<(std::ostream& os, const TTerm& dt)
{
    return os << "< TTerm term: " << dt.term << " subterms " << dt.subterms << " >";
}

bool VTerm::operator==(const VTerm& other) const
{
    return this->varname == other.varname;
}

std::ostream& operator<<(std::ostream& os, const VTerm& dt)
{
    os << "< VTerm variable name: " << dt.getVariableName() << " >";
    return os;
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
