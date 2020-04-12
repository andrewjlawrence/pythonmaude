cmake_minimum_required(VERSION 3.17)
set(BOOST_ROOT /Users/andrewlawrence/Tools/boost_1_72_0)
find_package (Boost COMPONENTS system filesystem unit_test_framework REQUIRED)
include_directories (${TERMREWRITING_SOURCE_DIR}/inc
                     ${Boost_INCLUDE_DIRS}
                     )

add_definitions (-DBOOST_TEST_DYN_LINK)
add_executable (Test variablenametests.cpp termtests.cpp substitutiontests.cpp termrewritingtests.cpp main.cpp)
target_link_libraries (Test
                       termrewriting
                       ${Boost_FILESYSTEM_LIBRARY}
                       ${Boost_SYSTEM_LIBRARY}
                       ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY}
                       )
