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

bool VTerm::operator==(const VTerm& other) const
{
    return this->varname == other.varname;
}