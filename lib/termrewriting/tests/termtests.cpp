#include <boost/test/unit_test.hpp>
#include "term.hpp"
#include "vterm.hpp"
#include "tterm.hpp"

BOOST_AUTO_TEST_CASE(VTermTest)
{
    VariableName vname("cat",1);
    VTerm vterm(vname);
    BOOST_TEST(vterm.occurs(vname));
}

BOOST_AUTO_TEST_CASE(TTermTest)
{
    VariableName vname("cat",1);
    VTerm vterm(vname);
    TermList_t subterms;
    subterms.push_back(vterm);
    TTerm tterm(std::string("dog"), subterms);
    BOOST_TEST(tterm.occurs(vname));
}
