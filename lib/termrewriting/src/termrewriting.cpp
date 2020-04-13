
#include "termrewriting.hpp"

Substitution TermRewriting::matchs(const RewriteSystem_t& rewriteSystem,
                                   const Substitution& substitution)
{
    if (!rewriteSystem.empty())
    {
        if(rewriteSystem[0].first.which() == VTerm_e)
        {
            const VariableName& varname = 
                rewriteSystem[0].first.asVTerm().getVariableName();
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
            const TTerm& ltterm = rewriteSystem[0].first.asTTerm();
            const TTerm& rtterm = rewriteSystem[0].second.asTTerm(); 
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
        TTerm tterm = term.asTTerm();
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
