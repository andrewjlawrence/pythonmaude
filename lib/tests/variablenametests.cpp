#include <boost/test/unit_test.hpp>
#include "variablename.hpp"

BOOST_AUTO_TEST_CASE(FailTest)
{
  VariableName varname(std::string("cat"),1);
  BOOST_TEST(varname.getName() == "cat");
}

