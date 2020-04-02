
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

const Term_t Substitution::app(const VTerm& vterm) const
{
    auto assoItr = std::find_if(associationList.begin(),
                             associationList.end(),
                             [&vterm](const Association_t& asso){
                                return asso.first == vterm.getVariableName();
                             });

    if (assoItr != associationList.end())
    {
        return (*assoItr).second;
    }
    else
    {
        return vterm;
    }
}

const Term_t Substitution::lift(Term_t& term) const
{
    switch (term.which())
    {
    case VTerm_e:
        return app(boost::get<VTerm>(term));
    case TTerm_e:
        for (size_t i = 0; i < boost::get<TTerm>(term).getSubterms().size(); i++ )
        {
            boost::get<TTerm>(term)[i] = lift(boost::get<TTerm>(term)[i]);
        }
        return term;
    default:
        return term;
    }
}