#include "variablename.hpp"

VariableName::VariableName(const std::string& name,
                           const uint32_t index)
    :name(name), index(index)
{
}

const std::string& VariableName::getName() const
{
    return name;
}

const u_int32_t VariableName::getIndex() const
{
    return index;
}

bool VariableName::operator==(const VariableName& other) const
{
    return this->name == other.name && this->index == other.index;
}

std::ostream& operator<<(std::ostream& os, const VariableName& varname)
{
    return os << varname.getName();
}
