#include "vterm.hpp"
#include <sstream>

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

const std::string VTerm::toString() const
{
    std::stringstream output;
    output << "< VTerm variablename: " << varname << " >";
    return output.str();
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