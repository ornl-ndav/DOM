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


    def __eq__(self, other):
        try:

            if self.instrument != other.instrument:
                return False

            if self.sample != other.sample:
                return False

        except:
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)
