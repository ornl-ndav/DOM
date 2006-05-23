import instrument

class CompositeInstrument(instrument.Instrument):
    """
    This class creates a collection of instrument objects. The individual
    instruments a accessed via an internal hash according to a given
    instrument key. The member function call is then passed onto the
    appropriate instrument object.
    """
    
    def __init__(self,*args,**kwargs):
        """
        Constructor for class. Keys and instruments can be passed as a list
        of arguments or via a list provided to the keyword "pair".

        Parameters:
        ----------
        -> args is a listing of key (string), instrument pairs
        -> kwargs is a list of key word arguments that the constructor will
           accept
              pairs=["key1",inst1,"key2",inst2]
        """
        
        self.__inst_hash = {}

        pairlist = []
        if len(args) > 0:
            if len(args) % 2 != 0:
                raise RuntimeError, "The list of arguments must be pairwise "\
                      +"and proceed as: key1, inst1, key2, inst2 ..."
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

        if len(pairlist) != 0:
            for i in range(0,len(pairlist),2):
                self.__inst_hash[pairlist[i]] = pairlist[i+1]
        # No arguments or keywords given, do nothing
        else:
            pass
        

    def set_instrument(self,key,obj):
        """
        This function sets the instrument object to the given key name in the
        internal hash.

        Parameters:
        ----------
        -> key is a string containing the given key name for the instrument
        -> obj is the given instrument object
        """
        
        self.__inst_hash[key] = obj


    def get_instrument(self,key,**kwargs):
        """
        This function returns the instrument assigned to the given key in the
        internal hash.

        Parameters:
        ----------
        -> key is a string containing the given key name for the instrument
        -> kwargs is a list of key word arguments that the function will accept

        Returns:
        -------
        <- The instrument object associated with the given key
        """
        
        return self.__inst_hash[key]


    def get_primary(self,id=None,**kwargs):
        """
        This function obtains the primary flight path from the instrument
        object. If no ID is passed to the function, it returns the primary
        flight path from the 

        Parameters:
        ----------
        -> id is the object containing the pixel ID
        -> kwargs is a list of key word arguments that the function will
           accept        

        Returns:
        -------
        <- A tuple containing the primary flight path and its associated error
           for the request instrument
        """

        if id == None:
            tag = self.__inst_hash.keys()[0]
        else:
            tag = id[0]

        return self.__inst_hash[tag].get_primary(id,**kwargs)

    
    def get_secondary(self,id,**kwargs):
        """
        This function obtains the secondary flight path from the instrument
        object.

        Parameters:
        ----------
        -> id is the object containing the pixel ID
        -> kwargs is a list of key word arguments that the function will
           accept        

        Returns:
        -------
        <- A tuple containing the secondary flight path and its associated
           error for the request instrument
        """

        return self.__inst_hash[id[0]].get_secondary(id,**kwargs)


    def get_total_path(self,id,**kwargs):
        """
        This function obtains the total flight path from the instrument
        object.

        Parameters:
        ----------
        -> id is the object containing the pixel ID
        -> kwargs is a list of key word arguments that the function will
           accept        

        Returns:
        -------
        <- A tuple containing the total flight path and its associated
           error for the request instrument
        """

        return self.__inst_hash[id[0]].get_total_path(id,**kwargs)


    def get_polar(self,id,**kwargs):
        """
        This function obtains the polar angle from the instrument object.

        Parameters:
        ----------
        -> id is the object containing the pixel ID
        -> kwargs is a list of key word arguments that the function will
           accept        

        Returns:
        -------
        <- A tuple containing the polar angle and its associated error
           for the request instrument
        """

        return self.__inst_hash[id[0]].get_polar(id,**kwargs)


    def get_azimuthal(self,id,**kwargs):
        """
        This function obtains the azimuthal angle from the instrument object.

        Parameters:
        ----------
        -> id is the object containing the pixel ID
        -> kwargs is a list of key word arguments that the function will
           accept        

        Returns:
        -------
        <- A tuple containing the azimuthal angle and its associated error
           for the request instrument
        """

        return self.__inst_hash[id[0]].get_azimuthal(id,**kwargs)
