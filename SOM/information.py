class Information:
    """
    This is a collector class used for storing information that is not pure
    instrument geometry information. The class contains members for a list
    of values, a list of errors and an index selector object. This object
    will be used for things like detector efficiencies, energy offset
    corrections (BSS), final wavelengths (BSS) and other pieces of information
    of this sort.
    """
    def __init__(self, value, err2, units, selector, **kwargs):
        """
        Class constructor
        
        Parameters:
        ----------
        -> value is a list containing the values associated with the
           information
        -> err2 is a list of uncertainties squared associated with the list of
           values
        -> selector is a string containing the name of an index selector
        -> kwargs is a list of key word arguments. This list is reserved for
           the use of passing key words arguments to the index selectors
        """
           
        import indexselector 
        
        self.__value__ = value
        self.__err2__ = err2
        self.__units__ = units
	self.__selector__ = indexselector.getIndexSelector(selector, **kwargs)

    def get_value(self, id, **kwargs):
        """
        This function returns a tuple containing the value and error2
        processed from the selector via the given id. If no error2 list is
        present, the error2 given in the returned tuple is 0.

        Parameters:
        ----------
        -> id is an object containing the pixel ID to be checked by the index
           selector

        Returns:
        -------
        <- A tuple containing the value and error2 associated with the given
           id

        Exceptions:
        ----------
        <- RuntimeError is raised if no index selector was provided to the
           object
        <- RuntimeError is raised if no value list was provided to the object
        """
        
        try:
            offset = self.__selector__.getIndex(id)
        except AttributeError:
            raise RuntimeError("Do not have information for selecting value")

        try:
            val = self.__value__[offset]
        except TypeError:
            raise RuntimeError("Do not have information for value")

        try:
            err2 = self.__err2__[offset]
            return (val, err2)
        except TypeError:
            return (val, 0.)


    def __str__(self):
        import os

        result = []
        
        result.append("Units: %s\tSelector: %s" % (self.__units__,
                                                   self.__selector__))

        length = len(self.__value__)
        result.append("Value: %s" % self.__value__.__str__(length))

        try:
            result.append("Error^2: %s" % self.__err2__.__str__(length))
        except TypeError:
            result.append("Error^2: %s" % str(self.__err2__))
        
        return os.linesep.join(result)
    
        
class CompositeInformation(Information):
    """
    This class creates a collection of information objects. The individual
    information objects are accessed via an internal hash according to a given
    information key. The member function call is then passed onto the
    appropriate information object.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Constructor for class. Keys and informations can be passed as a list
        of arguments or via a list provided to the keyword "pair".

        Parameters:
        ----------
        -> args is a listing of key (string), information pairs
        -> kwargs is a list of key word arguments that the constructor will
           accept
              pairs=["key1",info1,"key2",info2]
        """
        
        self.__info_hash = {}

        pairlist = []
        if args:
            if len(args) % 2 != 0:
                raise RuntimeError("The list of arguments must be pairwise "\
                                   +"and proceed as: key1, info1, "\
                                   +"key2, info2 ...")
            # Everything is OK, go on
            else:
                pass

            pairlist.extend(args)

        else:
            try:
                pairlist = kwargs["pairs"]
            # If key is not present, don't do anything
            except KeyError:
                pass

        if pairlist:
            for i in range(0,len(pairlist),2):
                self.__info_hash[pairlist[i]] = pairlist[i+1]
        # No arguments or keywords given, do nothing
        else:
            pass
        

    def set_information(self, key, obj):
        """
        This function sets the information object to the given key name in the
        internal hash.

        Parameters:
        ----------
        -> key is a string containing the given key name for the information
        -> obj is the given information object
        """
        
        self.__info_hash[key] = obj


    def get_information(self, key, **kwargs):
        """
        This function returns the information assigned to the given key in the
        internal hash.

        Parameters:
        ----------
        -> key is a string containing the given key name for the information
        -> kwargs is a list of key word arguments that the function will accept

        Returns:
        -------
        <- The information object associated with the given key
        """
        
        return self.__info_hash[key]

    def get_value(self, id, **kwargs):
        """
        This function obtains the value, error2 tuple from the information
        object.

        Parameters:
        ----------
        -> id is the object containing the pixel ID
        -> kwargs is a list of key word arguments that the function will
           accept        

        Returns:
        -------
        <- A tuple containing the value and its associated error2 for the
           request information object
        """

        return self.__info_hash[id[0]].get_value(id, **kwargs)


    def __str__(self):
        import os

        result = []

        for key in self.__info_hash.keys():
            result.append("%s: %s" % (key, str(self.__info_hash[key])))

        return os.linesep.join(result)


if __name__ == "__main__":
    import nessi_list

    val = nessi_list.NessiList()
    err2 = nessi_list.NessiList()

    val.extend(1.0,2.0)
    err2.extend(0.5,0.4)

    info1 = Information(val, None, "meter", "ZSelector")

    print "Info:",info1

    info2 = Information(val, err2, "meter", "ZSelector")

    comp = CompositeInformation("bank1", info1, "bank2", info2)

    print "CompInfo:",comp
