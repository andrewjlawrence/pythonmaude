cmake_minimum_required(VERSION 3.9)
project(termrewriting VERSION 0.0.1 DESCRIPTION "Term rewriting library")
SET(BOOST_ROOT "/Users/andrewlawrence/Tools/boost_1_72_0")
find_package(PythonLibs 3 REQUIRED)
find_package (Boost COMPONENTS system filesystem unit_test_framework python3.8 REQUIRED)
message(STATUS "Boost_LIBRARIES = ${Boost_LIBRARIES}")
message(STATUS "Boost_Python = ${Boost_PYTHON3.8_LIBRARY}")
                 
set(CMAKE_CXX_STANDARD 17)

add_library(termrewriting STATIC src/termrewriting.cpp src/variablename.cpp src/term.cpp src/substitution.cpp)
include_directories(${Boost_INCLUDE_DIRS})
target_include_directories(termrewriting PUBLIC inc  )
add_subdirectory(tests)

enable_testing ()
add_test (NAME MyTest COMMAND Test)

# Boost python seems OK but I am going to try Cython to see if it is better.
#python_add_module(pytermrewriting src/pythondefs.cpp)
#target_include_directories(pytermrewriting PUBLIC inc  ${PYTHON_INCLUDE_DIR})
#target_link_libraries (pytermrewriting
#                       termrewriting
#                       ${Boost_PYTHON3.8_LIBRARY}
#                       ${PYTHON_LIBRARY}
#                       )
