
#include "termrewriting.hpp"

Substitution TermRewriting::matchs(const RewriteSystem_t& rewriteSystem,
                                   const Substitution& substitution)
{
    if (!rewriteSystem.empty())
    {
        if(rewriteSystem[0].first.which() == VTerm_e)
        {
            const VariableName& varname = 
                boost::get<VTerm>(rewriteSystem[0].first).getVariableName();
            if(substitution.inDomain(varname))
            {
                if (substitution.app(varname) == rewriteSystem[0].second)
                {
                    RewriteSystem_t newRewriteSystem = rewriteSystem;
                    newRewriteSystem.erase(newRewriteSystem.begin());
                    return matchs(newRewriteSystem, substitution);
                }
                else
                    throw UnificationError("meh");
            }
            else
            {
                Substitution newSubstitution = substitution;
                newSubstitution.addMapping(varname,
                                            rewriteSystem[0].second);
                RewriteSystem_t newRewriteSystem = rewriteSystem;
                newRewriteSystem.erase(newRewriteSystem.begin());
                return matchs(newRewriteSystem, newSubstitution);
            }
            
        }
        else if (rewriteSystem[0].second.which() == VTerm_e)
        {
            throw UnificationError("meh");
        }
        else
        {
            std::cout << std::string("matchs on tterm") << std::endl;
            const TTerm& ltterm = boost::get<TTerm>(rewriteSystem[0].first);
            const TTerm& rtterm = boost::get<TTerm>(rewriteSystem[0].second); 
            if (ltterm.getTerm() == rtterm.getTerm())
            {
                RewriteSystem_t newSystem;
                for (size_t i = 0;
                     i < ltterm.getSubterms().size() && i < rtterm.getSubterms().size();
                     i++)
                {
                    newSystem.push_back(std::pair<Term_t, Term_t>(ltterm[i], rtterm[i]));
                }

                for (int i = 1;
                     i < rewriteSystem.size();
                     i++)
                {
                    newSystem.push_back(rewriteSystem[i]);
                }

                std::cout << std::string("new system size ") << newSystem.size() << std::endl;
                return matchs(newSystem, substitution);
            }
            else
            {
                throw UnificationError("meh");
            }
        }
        
    }
    else
    {
        return substitution;
    }
}

Substitution TermRewriting::match(const Term_t& pat, const Term_t& obj)
{
    return matchs({{pat,obj}}, Substitution());
}

Term_t TermRewriting::rewrite(const RewriteSystem_t& termlist, const Term_t& term)
{
    if (!termlist.empty())
    {
        try
        {
            return match(termlist[0].first, term).lift(termlist[0].second);
        }
        catch(const UnificationError& err)
        {
            RewriteSystem_t newSystem = termlist;
            newSystem.erase(newSystem.begin());
            return rewrite(newSystem, term);
        }
    }
    else
        throw NormalizationError("meh");
}

Term_t TermRewriting::normalize(const RewriteSystem_t& termlist, const Term_t& term)
{
    if (term.which() == VTerm_e)
    {
        std::cout << "Normalized vterm" << std::endl;
        return term;
    }
    else
    {
        TTerm tterm = boost::get<TTerm>(term);
        for (int i = 0; i < tterm.getSubterms().size(); i++)
        {
            std::cout << "Normalizing subterm" << std::endl;
            tterm[i] = normalize(termlist, tterm[i]);
        }

        try
        {
            std::cout << "Normalizing term: " << term << std::endl;
            return normalize(termlist, rewrite(termlist,tterm));
        }
        catch(const NormalizationError& e)
        {
            std::cerr << e.what() << '\n';
            return tterm;
        }
        
    }
    
}

UnificationError::UnificationError(const std::string msg)
:std::exception()
{
}

NormalizationError::NormalizationError(const std::string msg)
:std::exception()
{

}

#if 0
def matchs(termpairlist : List[Tuple[Term, Term]],  subst : Substitution) -> Substitution:
    if not termpairlist:
        return subst
    elif type(termpairlist[0][0]) == VTerm:
        if subst.indom(termpairlist[0][0].vname):
            if subst.apply(termpairlist[0][0].vname) == termpairlist[0][1]:
                return matchs(termpairlist[1:], subst)
            else:
                raise UnificationError("meh")
        else:
            subst.add_mapping(termpairlist[0][0].vname, termpairlist[0][1])
            return matchs(termpairlist[1:], subst)
    elif type(termpairlist[0][1]) == VTerm:
        raise UnificationError("meh")
    else:
        assert type(termpairlist[0][0]) == TTerm
        assert type(termpairlist[0][1]) == TTerm
        if termpairlist[0][0].term == termpairlist[0][1].term:
            return matchs(list(zip(termpairlist[0][0].termlist, termpairlist[0][1].termlist)) + termpairlist[1:], subst)
        else:
            raise UnificationError("meh")

class NormalizationError(Exception):
    def __init__(self, message):
        self.message = message


def match(pat : Term, obj : Term) -> Substitution:
    return matchs([(pat, obj)], Substitution())


def rewrite(termlist : List[Tuple[Term, Term]], term : Term) -> Term:
    if termlist:
        try:
            return match(termlist[0][0], term).lift(termlist[0][1])
        except UnificationError:
            return rewrite(termlist[1:], term)
    else:
        raise NormalizationError("meh")


def normalize(termlist, term):
    if type(term) == VTerm:
        return term
    else:
        newlist = list()
        for termtonormalize in term.termlist:
            newlist.append(normalize(termlist,termtonormalize))
        term.termlist = newlist
        try:
            return normalize(termlist, rewrite(termlist, term))
        except NormalizationError:
            return term
#endif