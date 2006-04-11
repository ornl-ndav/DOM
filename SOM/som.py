import attribute

class SOM(list):
    EMPTY   = ""

    def __init__(self):
        self.__title__ = SOM.EMPTY
        self.__axis_labels__ = []
        self.__axis_units__ = []
        self.__y_label__ = SOM.EMPTY
        self.__y_units__ = SOM.EMPTY
        self.__data_set_type__ = SOM.EMPTY
        
        self.attr_list = attribute.AttributeList()
        self.dst = None

    """
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(list)
        #return \"Title: \"+self.__title__+'\n'+str(list)
    """

    def copyAttributes(self,other):
        import copy
        
        self.setTitle(other.getTitle())
        self.setDataSetType(other.getDataSetType())
        self.setAllAxisLabels(other.getAllAxisLabels())
        self.setAllAxisUnits(other.getAllAxisUnits())
        self.setYLabel(other.getYLabel())
        self.setYUnits(other.getYUnits())
        self.attr_list = copy.copy(other.attr_list)
    
    def getAllAxisLabels(self):
        import copy
        return copy.copy(self.__axis_labels__)

    def getAllAxisUnits(self):
        import copy
        return copy.copy(self.__axis_units__)

    def getAxisLabel(self,dim=0):
        return self.__axis_labels__[dim]
    
    def getAxisUnits(self,dim=0):
        return self.__axis_units__[dim]

    def getDataSetType(self):
        return self.__data_set_type__

    def getDimension(self):
        return len(self.__axis_labels__)

    def getTitle(self):
        return self.__title__

    def getYLabel(self):
        return self.__y_label__

    def getYUnits(self):
        return self.__y_units__

    def hasAxisUnits(self,unit):
        """
        This function checks the array of primary axes for the requested units.
        If there are duplicate units, it will always find the first.
        
        Parameters:
        ----------
        -> unit is the string containg the name of the units to be searched for
        
        Returns:
        -------
        <- a boolean which is True if the units exist, False if it does not
        """

        return self.__axis_units__.contains(unit)

    def setAllAxisLabels(self,labels):
        self.__axis_labels__ = labels

    def setAllAxisUnits(self,units):
        self.__axis_units__ = units

    def setAxisLabel(self,dim,label):
        try:
            self.__axis_labels__[dim] = label
        except IndexError:
            self.__axis_labels__.append(label)            
    
    def setAxisUnits(self,dim,units):
        try:
            self.__axis_units__[dim] = units
        except IndexError:
            self.__axis_units__.append(units)            

    def setDataSetType(self,type):
        self.__data_set_type__ = type

    def setTitle(self,title):
        self.__title__ = title

    def setYLabel(self,label):
        self.__y_label__ = label

    def setYUnits(self,units):
        self.__y_units__ = units


        
if __name__ == "__main__":
    import so
    som = SOM()
    som.setTitle("Test SOM")
    som.setDataSetType("histogram")
    
    so1 = so.SO(withVar=True)
    so1.axis[0].val.extend([1.0,2.0,3.0])
    so1.axis[0].var.extend([1.0,2.0,3.0])
    so1.y.extend([40.0,55.0])
    so1.var_y.extend([40.0,55.0])
    so1.id="Pixel 1"

    axis_labels = ["Extent"]
    axis_units = ["centimeters"]

    som.setAllAxisLabels(axis_labels)
    som.setAllAxisUnits(axis_units)
    som.setYLabel("Counts")
    som.setYUnits("a.u.")
    som.append(so1)

    print "SOM:",som
    print "Title:",som.getTitle()
    print "Primary Axes:",som.getAllAxisLabels(),som.getAllAxisUnits()
