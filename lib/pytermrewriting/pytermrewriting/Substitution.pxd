
from libcpp.string cimport string
from libc cimport stdint
from libcpp cimport bool
cimport VariableName
cimport Term
cimport VTerm

# Now define the term class.
cdef extern from "Substitution.hpp":
    cdef cppclass Substitution:
        addMapping(const VariableName&,
                   const Term&)
        bool inDomain(const VariableName&) const
        const Term app(const VTerm&) const
        const Term lift(const Term&) const
