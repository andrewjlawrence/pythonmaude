from libcpp.string cimport string
from libc cimport stdint
from libcpp cimport bool
from libcpp cimport vector
cimport Term
cimport VariableName

# Forward declare the TTerm and VTerm classes
cdef extern from "tterm.hpp":
    cdef cppclass TTerm:
        TTerm(const string& termname, const vector[Term]& subterms)
        const string& getTerm() const
        const vector[Term]&  getSubterms() const
        Term& operator[](size_t index)
        const Term& operator[](size_t index) const
        bool occurs(const VariableName& vname) const
        bool operator==(const TTerm& other) const
        std::string toString() const
    