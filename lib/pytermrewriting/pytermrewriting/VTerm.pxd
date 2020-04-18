from libcpp.string cimport string
from libc cimport stdint
from libcpp cimport bool
cimport VariableName

cdef extern from "vterm.hpp":
    cdef cppclass VTerm:
        VTerm(const VariableName&)
        const VariableName& getVariableName() const
        bool occurs(const VariableName& vname) const
        bool operator==(const VTerm& other) const
        const string toString() const