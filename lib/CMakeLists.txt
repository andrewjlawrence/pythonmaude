cmake_minimum_required(VERSION 3.9)
SET(BOOST_ROOT "/Users/andrewlawrence/Tools/boost_1_72_0")
find_package (Boost COMPONENTS system filesystem unit_test_framework REQUIRED)
set(CMAKE_CXX_STANDARD 17)

project(termrewriting VERSION 0.0.1 DESCRIPTION "Term rewriting library")
add_library(termrewriting  src/termrewriting.cpp src/variablename.cpp src/term.cpp src/substitution.cpp)
include_directories(${Boost_INCLUDE_DIRS})
target_include_directories(termrewriting PUBLIC inc  )
add_subdirectory(tests)

enable_testing ()
add_test (NAME MyTest COMMAND Test)
