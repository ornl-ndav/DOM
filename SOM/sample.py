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

class Sample(object):
    """
    This is an abstract base class representing important information about
    the sample.

    @ivar name: The name of the sample
    @type name: C{string}

    @ivar nature: The type of sample
    @type nature: C{string}

    @ivar identifier: Serial number or other ID tagging scheme
    @type identifier: C{string}

    @ivar holder: The type of holder for the sample
    @type holder: C{string}

    @ivar changer_position: The location of the sample in a sample changer
    @type changer_position: C{string}

    @ivar __empty_content: The types of empty content
    @type __empty_content: C{list} of C{string}s
    """
    def __init__(self):
        """
        Object constructor
        """
        self.name =  ""
        self.nature = ""
        self.identifier = ""
        self.holder = ""
        self.changer_position = ""
        self.__empty_content = ["", " ", "NONE"]

    def __is_empty(self, value):
        """
        This method checks the content to see if of the empty variety.

        @param value: The value to check for emptiness
        @type value: C{string}


        @return: State of the value's emptiness
        @rtype: C{boolean}
        """
        return value in self.__empty_content or value is None

    def __str__(self):
        """
        The string representation of the class.

        @return: The string representation of the class.
        @rtype: C{string}
        """
        result = []
        if not self.__is_empty(self.name):
            result.append("Name; "+self.name)
        if not self.__is_empty(self.nature):
            result.append("|")
            result.append("Nature; "+self.nature)
        if not self.__is_empty(self.identifier):
            result.append("|")
            result.append("Identifier; "+self.identifier)
        if not self.__is_empty(self.holder):
            result.append("|")
            result.append("Holder; "+self.holder)
        if not self.__is_empty(self.changer_position):
            result.append("|")
            result.append("Changer Position; "+self.changer_position)

        return " ".join(result)

    def __eq__(self, other):
        """
        This method checks to see if the incoming C{Sample} object and current
        one are equal.

        @param other: Object to check for equality
        @type other: C{Sample}

        @return: I{True} is the C{Sample} objects are equal, I{False} if they
                 are not.
        @rtype: C{boolean}
        """
        is_equal = False
        for key in self.__dict__:
            if "Sample" in key:
                continue
            if self.__dict__[key] == other.__dict__[key]:
                is_equal = True
            else:
                is_equal = False

        return is_equal

    def __ne__(self, other):
        """
        This method checks to see if the incoming C{Sample} object and current
        one are not equal.

        @param other: Object to check for inequality
        @type other: C{Sample}

        @return: I{True} is the C{Sample} objects are not equal, I{False} if
                 they are.
        @rtype: C{boolean}        
        """
        return not self.__eq__(other)

    def fromString(cls, istr):
        """
        This method provides an alternative constructor method for creating a
        L{SOM.Sample} from a C{string} representation of the object.
        
        @param istr: Object containing the string representation
        @type istr: C{string}
        
        
        @return: A new object with the information from the C{string}
        @rtype: L{SOM.Sample}
        """
        parts = istr.split('|')
        sample = Sample()
        for part in parts:
            temp = part.split(';')
            key = temp[0].strip()
            value = temp[1].strip()
            if "Name" in key:
                sample.name = value
            elif "Nature" in key:
                sample.nature = value
            elif "Identifier" in key:
                sample.identifier = value
            elif "Holder" in key:
                sample.holder = value
            elif "Changer Position" in key:
                sample.changer_position = value            
                
        return sample

    fromString = classmethod(fromString)
