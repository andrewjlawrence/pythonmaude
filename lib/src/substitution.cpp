
#include "substitution.hpp"

void Substitution::addMapping(const VariableName& vname,
                              const Term_t& term)
{
    associationList.push_back(Association_t(vname,term));
}

bool Substitution::inDomain(const VariableName& vname) const
{
    return std::any_of(associationList.begin(),
                       associationList.end(),
                       [&vname](const Association_t& assoc){
                           return vname == assoc.first;
                       });
}