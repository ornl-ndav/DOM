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

class ParameterMap:
    """
    This is a simple class that has an internal hash table that keeps
    L{Parameter} objects in it. The L{Parameter} objects contain the end path
    location of the information in the NeXus file.

    @ivar __pmap: Hash table for C{Parameter} objects
    @type __pmap: C{dict}
    """
    
    def __init__(self):
        """
        Class constructor. Initializes all of the currently mapped parameters.
        """
        self.__pmap = {}

        self.__pmap["proton_charge"] = Parameter("proton_charge", "float")
        self.__pmap["raw_frames"] = Parameter("raw_frames", "int")
        self.__pmap["total_counts"] = Parameter("total_counts", "int")

    def getPathAndType(self, name):
        """
        Method that returns a tuple containing NeXus path and the type
        (C{float}, C{int}, C{string} etc.) that the information should be
        presented as.

        @param name: The key name that the parameter map will use to return
                     the path and type.
        @type name: C{string}


        @returns: The path and type for the parameter
        @rtype: C{tuple}
        """
        return (self.__pmap[name].getPath(),
                self.__pmap[name].getType())

class Parameter:
    """
    This is a simple class that contains two pieces of information about a
    given parameter. The pieces of information are the path in the NeXus file
    of the parameter data and the primitive type of the parameter.

    @ivar __path: The final element of the NeXus path for the parameter
    @type __path: C{string}

    @ivar __type: The classification of the parameter value type. This can
                  be C{float}, C{int}, C{string} etc.
    @type __type: C{string}
    """
    
    def __init__(self, path, type):
        """
        Class constructor

        @param path: The NeXus path for the parameter
        @type path: C{string}
        
        @param type: The type of the parameter
        @type type: C{string}
        """
        self.__path = path
        self.__type = type

    def getPath(self):
        """
        Method that returns the NeXus path

        @returns: The NeXus path
        @rtype: C{string}
        """
        return self.__path

    def getType(self):
        """
        Method that returns the parameter type

        @returns: The type for the parameter
        @rtype: C{string}
        """
        return self.__type

