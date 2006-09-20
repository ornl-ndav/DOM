# $Id$

class ParameterMap:
    """
    This is a simple class that has an internal hash table that keeps Parameter
    objects in it. The Parameter objects contain the end path location of the
    information in the NeXus file. 
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
        Function that returns a tuple containing NeXus path and the type
        (float, int, string etc.) that the information should be presented as.

        Parameters:
        ----------
        -> name is a string containing the key name that the parameter map
           will use to return the path and type

        Returns:
        -------
        <- A tuple containing the path and type for the parameter
        """
        return (self.__pmap[name].getPath(),
                self.__pmap[name].getType())


class Parameter:
    """
    This is a simple class that contains two pieces of information about a
    given parameter. The pieces of information are the path in the NeXus file
    of the parameter data and the primitive type of the parameter.
    """
    def __init__(self, path, type):
        """
        Class constructor

        Parameters:
        ----------
        -> path is a string containing the NeXus path for the parameter
        -> type is a string containing the type of the parameter
        """
        self.__path = path
        self.__type = type

    def getPath(self):
        """
        Function that returns the NeXus path

        Returns:
        -------
        <- A string containing the NeXus path
        """
        return self.__path

    def getType(self):
        """
        Function that returns the parameter type

        Returns:
        -------
        <- A string containing the type for the parameter
        """
        return self.__type

