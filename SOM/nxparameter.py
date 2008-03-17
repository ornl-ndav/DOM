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

class NxParameter(object):
    """
    This class represents U{NeXus<www.nexusformat.org>} parameters stored in a
    U{NeXus<www.nexusformat.org>} file. A given parameter may or may not have
    units associated with it. The ability to add similar parameters together
    will be a key feature of this class. The values of the C{NxParameter}
    class are designed to be C{string}s, C{float}s or C{int}s. The class does
    not understand how to deal with anything else.

    @ivar __value: The value for a given NeXus parameter
    @type __value: C{string}, C{float} or C{int}

    @ivar __units: The units for the NeXus parameter
    @type __units: C{string}

    @ivar __val_type: The primitive type for the NeXus parameter
    @type __val_type: C{string}
    """

    def __init__(self, value, units=None):
        """
        Object constructor

        @param value: Value to be stored
        @type value: C{string}, C{float} or C{int}
        @param units: The associated units for the value (can be C{None})
        @type units: C{string} or C{None}
        """
        self.__value = value
        self.__units = units
        self.__val_type = type(self.__value)

    def getUnits(self):
        """
        This method gets the units associated with the parameter

        @return: Associated parameter units
        @rtype: C{string}
        """
        return self.__units

    def getValue(self):
        """
        This method gets the value of the parameter

        @return: The parameter value
        @rtype: C{string}, C{float} or C{int}
        """
        return self.__value

    def isCompatible(self, other):
        """
        This method checks a given C{NxParameter} object against the current
        one and returns a C{boolean} answer about compatibility.

        @param other: Object to check for compatibility
        @type other: C{SOM.NxParameter} 


        @return: The value depending on the check for compatiblity
        @rtype: C{boolean}
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
        This method provides a string representation of C{NxParameter}. If
        units are present, the representation is turned into a C{tuple}.

        @return: The representation of the value and units (if applicable)
        @rtype: C{string}
        """
        if self.__units is None:
            return str(self.__value)
        else:
            return str((self.__value, self.__units))

    def __repr__(self):
        """
        This method provides a representation of the C{NxParameter}

        @return: The representation of the C{NxParameter}. It uses X{__str__}.
        @rtype: C{string}
        """
        return self.__str__()


    def __add__(self, right):
        """
        This method allows the addition of two C{NxParameter} objects. A
        warning is generated if the two objects are not compatible and the
        original object is returned.

            >>> obj3 = obj1 + obj2

        @param right: Object to add
        @param right: C{SOM.NxParameter}


        @return: The resulting object after addition
        @rtype: C{SOM.NxParameter}


        @raise RuntimeError: The value type is not recognized
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
        This method allows the addition of a scalar value to a C{NxParameter}
        object. A warning is generated if the scalar value and the
        C{NxParameter} are not compatible and the original C{NxParameter} is
        returned.

            >>> obj2 = \"Hi\" + obj1

        @param left: The primitive type or C{tuple:(primitive type, units)} to
                     add.
        @type left: C{string}, C{float}, C{int} or C{tuple}


        @return: The resulting object after addition
        @rtype: C{SOM.NxParameter} 


        @raise RuntimeError: The value type is not recognized
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
        This method allows the in place addition of a C{NxParameter} object
        with another C{NxParameter} object. A warning is generated if the two
        objects are not compatible and the original object is returned.

            >>> obj1 += obj2

        @param left: Object to add
        @type left: C{SOM.NxParameter}


        @return: The resulting object after addition
        @rtype: C{SOM.NxParameter}


        @raise RuntimeError: The value type is not recognized
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

    def fromString(cls, istr):
        """
        This method provides an alternative constructor method for creating a
        C{NxParameter} from a C{string} of either \"(value, units)\" or
        \"value, units\".
        
        @param obj: Object containing a value and units.
        @type obj: C{string}

        
        @return: A new object with the information from the C{string}
        @rtype: C{SOM.NxParameter}
        """
        parts = istr.lstrip('(').rstrip(')').split(',')
        vpart = parts[0].strip()
        if len(parts) < 2:
            upart = None
        else:
            upart = parts[1].strip().strip('\'')
        try:
            value = int(vpart)
        except ValueError:
            try:
                value = float(vpart)
            except ValueError:
                value = vpart

        return NxParameter(value, upart)

    fromString = classmethod(fromString)

def fromTuple(obj):
    """
    This method provides an alternative constructor method for creating a
    C{NxParameter} from a C{tuple} of the following form C{(value, units)}. A
    C{tuple} may be specified as following: C{(value, None)}.

    @param obj: Object containing a value and units.
    @type obj: C{tuple}


    @return: A new object with the information from the C{tuple}
    @rtype: C{SOM.NxParameter}
    """
    return NxParameter(obj[0], obj[1])

if __name__ == "__main__":
    
    par1 = NxParameter("Help")
    par2 = NxParameter("Help")
    par3 = NxParameter("Test")
    par4 = NxParameter(1.0, "crowns")
    par5 = NxParameter(2.0, "crowns")
    par6 = NxParameter(3.0, "pence")
    par7 = NxParameter.fromString("(1.032, seconds)")
    par8 = NxParameter.fromString("Testing")

    print "*************************"
    print "par1:", par1
    print "par2:", par2
    print "par3:", par3
    print "par4:", par4
    print "par5:", par5
    print "par6:", par6
    print "par7:", par7
    print "par8:", par8
    
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
