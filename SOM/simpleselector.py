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
