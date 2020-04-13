
from libcpp.string cimport string
from libc cimport stdint
from libcpp cimport bool

# Declare the class with cdef
cdef extern from <boost/variant.hpp> namespace boost:
    cdef cppclass variant[T1, T2]:
        variant() except +


# Declare the class with cdef
cdef extern from "term.hpp":
    cdef cppclass VariableName:
        VariableName() except +
        VariableName(const string&,
                     const stdint.uint32_t) except +
        const string& getName() const
        stdint.uint32_t getIndex() const
        const string& toString() const
        bool operator==(const VariableName&) const
