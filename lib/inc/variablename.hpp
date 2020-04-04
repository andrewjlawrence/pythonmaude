#ifndef VARIABLE_NAME_H
#define VARIABLE_NAME_H

#include <string>

/**
 *  A variable name consists of a 
 *  string and a numver for example x_1
 */
class VariableName
{
public:
    /**
     * Constructor for a variable name 
     */
    VariableName(const std::string& name,
                 const uint32_t index);
    /**
     * Accessor method for the variable name
     */
    const std::string& getName() const;

    /**
     * Comparison operator
     */
    bool operator==(const VariableName& other) const;

    /**
     * Accessor method for the index
     */
    const u_int32_t getIndex() const;

    /**
     * Friend output stream operator to print the variable name
     */
    friend std::ostream& operator<<(std::ostream& os, const VariableName& varname);
private:
    std::string name;
    u_int32_t index;
};

#endif 