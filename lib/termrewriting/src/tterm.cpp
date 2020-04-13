#include "tterm.hpp"
#include "vterm.hpp"
#include <sstream>

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
                    result = x.asVTerm().occurs(vname);
                    break;
                case TTerm_e: 
                    result = x.asTTerm().occurs(vname);
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

std::string TTerm::toString() const
{
    std::stringstream output;
    output << "< TTerm term: " << term << " subterms " << subterms << " >";
    return output.str();
}

std::ostream& operator<<(std::ostream& os, const TTerm& dt)
{
    return os <<  dt.toString();
}
