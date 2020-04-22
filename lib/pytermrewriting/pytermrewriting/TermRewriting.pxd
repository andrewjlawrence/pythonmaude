
from libcpp.string cimport string
from libc cimport stdint
from libcpp cimport bool
cimport VariableName
cimport Term
cimport VTerm

# Now define the term class.
cdef extern from "TermRewriting.hpp":
    cdef cppclass TermRewriting:
            @staticmethod
            Term normalize(const RewriteSystem_t& termlist, const Term& term);
