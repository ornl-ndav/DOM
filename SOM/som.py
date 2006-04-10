import attribute

class SOM(list):
    EMPTY   = ""

    def __init__(self):
        self.title = SOM.EMPTY
        self.axis_labels = []
        self.axis_units = []
        self.y_label = SOM.EMPTY
        self.y_units = SOM.EMPTY
        
        self.attr_list = attribute.AttributeList()
        self.dst = None

    def getAllAxisLabels(self):
        import copy
        return copy.copy(self.axis_labels)

    def getAllAxisUnits(self):
        import copy
        return copy.copy(self.axis_units)

    def getAxisLabel(self,dim=0):
        return self.axis_label[dim]
    
    def getAxisUnits(self,dim=0):
        return self.axis_units[dim]

    def getTitle(self):
        return self.title

    def getYLabel(self):
        return self.y_label

    def getYUnits(self):
        return self.y_units

    def setAllAxisLabels(self,labels):
        if len(self.axis_labels):
            self.axis_labels = []

        for label in labels:
            self.axis_labels.append(label)

    def setAllAxisUnits(self,units):
        if len(self.axis_units):
            self.axis_units = []

        for unit in units:
            self.axis_units.append(unit)

    def setAxisLabel(self,dim,label):
        self.axis_label[dim] = label
    
    def setAxisUnits(self,dim,units):
        self.axis_units[dim] = units

    def setTitle(self,title):
        self.title = title

    def setYLabel(self,label):
        self.y_label = label

    def setYUnits(self,units):
        self.y_units = units

        
if __name__ == "__main__":
    import so_base
    som = SOM()
    som.setTitle("Test SOM")
    
    so1 = so_base.SO(withVar=True)
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

    print "SOM: ",som
    print "Primary Axes:",som.getAllAxisLabels(),som.getAllAxisUnits()
