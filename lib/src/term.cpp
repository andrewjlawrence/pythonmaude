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
                case 0: 
                    result = boost::get<VTerm>(x).occurs(vname);
//                case 1: 
//                    result = boost::get<TTerm>(x).occurs(vname);
            }
            return result;
        }
    );
}

