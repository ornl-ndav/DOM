#                        Data Object Model
#           A part of the SNS Analysis Software Suite.
#
#                  Spallation Neutron Source
#          Oak Ridge National Laboratory, Oak Ridge TN.
#
#
#                             NOTICE
#
# For this software and its associated documentation, permission is granted
# to reproduce, prepare derivative works, and distribute copies to the public
# for any purpose and without fee.
#
# This material was prepared as an account of work sponsored by an agency of
# the United States Government.  Neither the United States Government nor the
# United States Department of Energy, nor any of their employees, makes any
# warranty, express or implied, or assumes any legal liability or
# responsibility for the accuracy, completeness, or usefulness of any
# information, apparatus, product, or process disclosed, or represents that
# its use would not infringe privately owned rights.
#

# $Id$

class NxParameter:
    """
    This class represents NeXus parameters stored in a NeXus file. A given 
    parameter may or may not have units associated with it. The ability to
    add similar parameters together will be a key feature of this class. The
    values of the NxParameter class are designed to be string, floats or ints.
    The class does not understand how to deal with anything else.
    """

    def __init__(self, value, units=None):
        """
        Object constructor

        Parameters:
        ----------
        -> value is a primitive type or object containing some information
        -> units is the associated units for the value (can be None)
        """
        self.__value = value
        self.__units = units
        self.__val_type = type(self.__value)

    def getUnits(self):
        """
        This method gets the units associated with the parameter

        Returns:
        -------
        <- Associated parameter units
        """
        return self.__units

    def getValue(self):
        """
        This method gets the value of the parameter

        Returns:
        -------
        <- The parameter value
        """
        return self.__value

    def isCompatible(self, other):
        """
        This method checks a given NxParamter object against the current one
        and returns a boolean answer about compatibility.

        Parameters:
        ----------
        -> other is a NxParameter to check for compatibility

        Return:
        ------
        <- A boolean value depending on the check for compatiblity
        """
        if self.__units is None:
            if self.__val_type == type(other.getValue()):
                return True
            else:
                return False
        else:
            if other.getUnits() is None:
                return False
            else:
                if self.__units == other.getUnits():
                    return True
                else:
                    return False

    def __str__(self):
        """
        This method provides a string representation of NxParameter. If units
        are present, the representation is turned into a tuple.

        Returns:
        -------
        <- The string representation of the value and units (if applicable)
        """
        if self.__units is None:
            return str(self.__value)
        else:
            return str((self.__value, self.__units))

    def __repr__(self):
        """
        This method provides a representation of the NxParameter

        Returns:
        -------
        -> A string representation of the NxParameter. It uses __str__.
        """
        return self.__str__()


    def __add__(self, right):
        """
        This method allows the addition of two NxParameter objects. A warning
        is generated if the two objects are not compatible and the original
        object is returned.

        obj3 = obj1 + obj2

        Parameters:
        ----------
        -> right is a NxParameter to add

        Returns:
        -------
        <- The resulting NxParameter after addition

        Exceptions:
        ----------
        <- RuntimeError is raised if the value type is not recognized
        """
        value = ""
        units = None
        if self.isCompatible(right):
            if self.__val_type is str:
                if not self.__value == right.getValue():
                    value = self.__value + " / " + right.getValue()
                else:
                    value = self.__value
            elif self.__val_type is float or self.__val_type is int:
                value = self.__value + right.getValue()
                if self.__units is not None:
                    units = self.__units
            else:
                raise RuntimeError("Do not know how to add %s" % \
                                   str(self.__val_type))

            return NxParameter(value, units)
        else:
            print "Parameters %s and %s are not compatible for adding" \
                  % (str(self), str(right))
            return self

    def __radd__(self, left):
        """
        This method allows the addition of a scalar value to a NxParameter
        object. A warning is generated if the scalar value and the NxParameter
        are not compatible and the original NxParameter is returned.

        obj2 = \"Hi\" + obj1

        Parameters:
        ----------
        -> left is a primitive type or tuple(primitive type, units)

        Returns:
        -------
        <- The resulting NxParameter after addition

        Exceptions:
        ----------
        <- RuntimeError is raised if the value type is not recognized
        """
        left_type = type(left)
        if left_type == NxParameter:
            return self+left
        elif left_type == tuple:
            return self+NxParameter.fromTuple(left)
        else:
            return self+NxParameter(left)

    def __iadd__(self, left):
        """
        This method allows the in place addition of a NxParameter object with
        another NxParameter object. A warning is generated if the two objects
        are not compatible and the original object is returned.

        obj1 += obj2

        Parameters:
        ----------
        -> left is a NxParameter to add

        Returns:
        -------
        <- The resulting NxParameter after addition

        Exceptions:
        ----------
        <- RuntimeError is raised if the value type is not recognized
        """
        if self.isCompatible(left):
            if self.__val_type is str:
                if not self.__value == left.getValue():
                    self.__value = self.__value + " / " + left.getValue()
            elif self.__val_type is float or self.__val_type is int:
                self.__value += left.getValue()
            else:
                raise RuntimeError("Do not know how to add %s" % \
                                   str(self.__val_type))
        else:
            print "Parameters %s and %s are not compatible for adding" \
                  % (str(self), str(left))

        return self

def fromTuple(obj):
    """
    This method provides an alternative constructor method for creating a
    NxParameter from a tuple of the following form (value, units). A tuple may
    be specified as following: (value, None)

    Parameters:
    ---------
    -> obj is a tuple containing a value and units.

    Returns:
    -------
    <- A new NxParameter object with the information from the tuple
    """
    return NxParameter(obj[0], obj[1])

if __name__ == "__main__":
    
    par1 = NxParameter("Help")
    par2 = NxParameter("Help")
    par3 = NxParameter("Test")
    par4 = NxParameter(1.0, "crowns")
    par5 = NxParameter(2.0, "crowns")
    par6 = NxParameter(3.0, "pence")

    print "*************************"
    print "par1:", par1
    print "par2:", par2
    print "par3:", par3
    print "par4:", par4
    print "par5:", par5
    print "par6:", par6
    
    print "par1+par2:", par1+par2
    print "par3+par1:", par3+par1
    print "par2+par3:", par2+par3
    par1 += par3
    print "par1+=par3:", par1
    print "par4+par5:", par4+par5
    print "par5+par6:", par5+par6
    par4 += par5
    print "par4+=par5:", par4
    print "\"Hi\"+par1:", "Hi"+par1
    print "3.0+par6:", 3.0+par6
    print "(3.0, \"pence\")+par6:", (3.0, "pence")+par6
