# distutils: language = c++

from VariableName cimport VariableName
from libcpp.string cimport string
from libc cimport stdint

cdef class PyVariableName:
    cdef VariableName c_varname  # Hold a C++ instance which we're wrapping

    def __cinit__(self, 
                  const string& name,
                  const stdint.uint32_t index):
        self.c_varname = VariableName(name, index)

    def get_name(self):
        return self.c_varname.getName()

    def get_index(self):
        return self.c_varname.getIndex()

    def __str__(self):
        return self.c_varname.getString()

    def __eq__(self, other):
        return self.c_varname.operator==(other.c_varname)