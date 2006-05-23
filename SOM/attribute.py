class AttributeList(dict):
    def __init__(self,**kwargs):
        """
        Parameters:
        -----------
        ->kwargs is a list of key word arguments that the function accepts:
             instrument = the instrument for the AttributeList to hold
             sample     = the sample for the AttributeList to hold
        """

        try:
            self.instrument=kwargs["instrument"]
        except KeyError:
            self.instrument=None

        try:
            self.sample=kwargs["sample"]
        except KeyError:
            self.sample=None
