
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

const Term_t Substitution::lift( const Term_t& term) const
{
    switch (term.which())
    {
    case VTerm_e:
        return app(boost::get<VTerm>(term));
    case TTerm_e:
    {
        TTerm tterm = boost::get<TTerm>(term);
        for (size_t i = 0; i < tterm.getSubterms().size(); i++ )
        {
            tterm[i] = lift(tterm[i]);
        }
        return tterm;
        break;
    }
    default:
        return term;
    }
}

std::ostream& operator<<(std::ostream& os, const Substitution& dt)
{
    os << "< Subst elemenst ";
    for (auto asso : dt.associationList)
    {
        os << " first " << asso.first;
        os << " second " << asso.second;
        os << " ";
    }
    os << " >";
    return os;
}