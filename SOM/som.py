import attribute

class SOM(list):
    TITLE   = "title"
    X_UNITS = "x_units"
    Y_UNITS = "y_units"
    EMPTY   = ""

    def __init__(self):
        self.attr_list = attribute.AttributeList()
        self.attr_list[SOM.TITLE]   = SOM.EMPTY
        self.attr_list[SOM.X_UNITS] = SOM.EMPTY
        self.attr_list[SOM.Y_UNITS] = SOM.EMPTY
        self.dst = None
