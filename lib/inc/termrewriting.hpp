#ifndef TERMREWRITING_H
#define TERMREWRITING_H
#include "substitution.hpp"

class TermRewriting
{
static Substitution matchs(const AssociationList_t& associationList,
                           const Substitution& substitution);

static Substitution match(const Term_t& pat, const Term_t& obj);
};

#endif