import indexselector

class ISelector(indexselector.IndexSelectorBase):
    """
    This class takes a NeXus spectrum ID and returns the index associated
    with the slowest varying position index.
    """

    def __init__(self,**kwargs):
        pass

    def getIndex(self, id):
        """
        Return the slowest varying pixel position index

        Parameters:
        ----------
        -> id is a NeXus spectrum ID

        Returns:
        -------
        <- The slowest varying pixel position index
        """
        
        return id[1][0]


    def __str__(self):
        return "ISelector"

class JSelector(indexselector.IndexSelectorBase):
    """
    This class takes a NeXus spectrum ID and returns the index associated
    with the fastest varying position index.
    """

    def __init__(self,**kwargs):
        pass

    def getIndex(self, id):
        """
        Return the fastest varying pixel position index

        Parameters:
        ----------
        -> id is a NeXus spectrum ID

        Returns:
        -------
        <- The fastest varying pixel position index
        """

        return id[1][1]

    def __str__(self):
        return "JSelector"

class ZSelector(indexselector.IndexSelectorBase):
    """
    This class always returns zero from the getIndex function
    """

    def __init__(self,**kwargs):
        pass

    def getIndex(self, id):
        """
        Always return zero not matter what the index is

        Parameters:
        ----------
        -> id is a NeXus spectrum ID

        Returns:
        -------
        <- 0
        """

        return 0

    def __str__(self):
        return "ZSelector"

class IJSelector(indexselector.IndexSelectorBase):
    """
    This class takes a NeXus spectrum ID and returns the index associated
    with the slowest varying position index.
    """

    def __init__(self,**kwargs):
        try:
            self.__N_j = int(kwargs["Nj"])
        except KeyError:
           raise RuntimeError, "Need to provide the number of pixels for the "\
                 +"fastest running index"
    

    def getIndex(self, id):
        """
        Return the slowest varying pixel position index

        Parameters:
        ----------
        -> id is a NeXus spectrum ID

        Returns:
        -------
        <- The slowest varying pixel position index
        """
        
        return id[1][1] + self.__N_j * id[1][0]

    def __str__(self):
        return "IJSelector (Nj=%d)" % self.__N_j
