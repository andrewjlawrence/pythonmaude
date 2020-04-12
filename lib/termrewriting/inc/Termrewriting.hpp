#ifndef TERMREWRITING_H
#define TERMREWRITING_H
#include "substitution.hpp"

class TermRewriting
{
public:
    using RewriteSystem_t = std::vector<std::pair<Term_t,Term_t>>;
    static Substitution matchs(const RewriteSystem_t& rewriteSystem,
                           const Substitution& substitution);

    static Substitution match(const Term_t& pat, const Term_t& obj);
    static Term_t rewrite(const RewriteSystem_t& termlist, const Term_t& term);
    static Term_t normalize(const RewriteSystem_t& termlist, const Term_t& term);
};

class UnificationError : public std::exception
{
public:
    UnificationError(const std::string msg);
};

class NormalizationError : public std::exception
{
public:
    NormalizationError(const std::string msg);
};

#endif