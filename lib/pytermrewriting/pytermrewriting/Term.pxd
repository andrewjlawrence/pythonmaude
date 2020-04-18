
from libcpp.string cimport string
from libc cimport stdint
from libcpp cimport bool

# Forward declare the TTerm and VTerm classes
cdef extern from "tterm.hpp":
    cdef cppclass TTerm:
        pass

cdef extern from "vterm.hpp":
    cdef cppclass VTerm:
        pass

# Now define the term class.
cdef extern from "term.hpp":
    cdef cppclass Term:
        Term() except +
        Term(const VTerm&) except +
        Term(const TTerm&)
        ~Term()
        int which() const
        const TTerm& asTTerm() const except +
        const VTerm& asVTerm() const except +
        Term& operator=(const TTerm&)
        Term& operator=(const VTerm&)
        bool operator==(const Term&) const
        string toString() const