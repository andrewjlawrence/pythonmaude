cmake_minimum_required(VERSION 3.9)
SET(BOOST_ROOT "/Users/andrewlawrence/Tools/boost_1_72_0")

project(termrewritng VERSION 0.0.1 DESCRIPTION "Term rewriting library")
target_include_directories(termrewriting PRIVATE inc)
add_library(termrewriting SHARED
    src/termrewriting.cpp
)
