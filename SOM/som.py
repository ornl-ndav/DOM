#                        Data Object Model
#           A part of the SNS Analysis Software Suite.
#
#                  Spallation Neutron Source
#          Oak Ridge National Laboratory, Oak Ridge TN.
#
#
#                             NOTICE
#
# For this software and its associated documentation, permission is granted
# to reproduce, prepare derivative works, and distribute copies to the public
# for any purpose and without fee.
#
# This material was prepared as an account of work sponsored by an agency of
# the United States Government.  Neither the United States Government nor the
# United States Department of Energy, nor any of their employees, makes any
# warranty, express or implied, or assumes any legal liability or
# responsibility for the accuracy, completeness, or usefulness of any
# information, apparatus, product, or process disclosed, or represents that
# its use would not infringe privately owned rights.
#

# $Id$

import attribute
from nxparameter import NxParameter

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

    def __eq__(self, other):
        try:
            if self.__title__ != other.getTitle():
                return False

            if self.__y_units__ != other.getYUnits():
                return False

            if self.__y_label__ != other.getYLabel():
                return False

            if self.__data_set_type__ != other.getDataSetType():
                return False

            if len(self.__axis_labels__) != other.getDimension():
                return False

            if self.__axis_labels__ != other.getAllAxisLabels():
                return False

            if self.__axis_units__ != other.getAllAxisUnits():
                return False

            if self.attr_list != other.attr_list:
                return False

        except:
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)
        
    def copyAttributes(self, other, add_nxpars=False):
        import copy
        
        self.setTitle(other.getTitle())
        self.setDataSetType(other.getDataSetType())
        self.setAllAxisLabels(other.getAllAxisLabels())
        self.setAllAxisUnits(other.getAllAxisUnits())
        self.setYLabel(other.getYLabel())
        self.setYUnits(other.getYUnits())
        if len(self.attr_list.keys()) == 0:
            self.attr_list = copy.copy(other.attr_list)
        else:
            self.attr_list.instrument = copy.copy(other.attr_list.instrument)
            self.attr_list.sample = copy.copy(other.attr_list.sample)

            if add_nxpars:
                nxpar_keys = [item[0] for item in self.attr_list.items() \
                              if isinstance(item[1], NxParameter)]

                for nxpar_key in nxpar_keys:
                    self.attr_list[nxpar_key] += other.attr_list[nxpar_key]
            else:
                # Do nothing
                pass
                    
            keys_to_get = [other_key for other_key in other.attr_list.keys() \
                           if other_key not in self.attr_list.keys()]
                
            for key_to_get in keys_to_get:
                self.attr_list[key_to_get] = \
                                       copy.copy(other.attr_list[key_to_get])

    def axisUnitsAt(self,units):
        return self.__axis_units__.index(units)
    
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

        return self.__axis_units__.__contains__(unit)

    def rekeyNxPars(self, dataset_tag):
        """
        This function prepends a dataset tag to the keys of NxParameters in
        the SOMs attribute list.

        Parameters:
        ----------
        -> dataset_tag is a string containing the name to prepend to the key
        """
        nxpar_keys = [item[0] for item in self.attr_list.items() \
                      if isinstance(item[1], NxParameter)]
        
        nxpar_values = []
        for nxpar_key in nxpar_keys:
            nxpar_values.append(self.attr_list.pop(nxpar_key))

        import itertools
        for nxpar_rekeyed in itertools.izip(nxpar_keys, nxpar_values):
            self.attr_list[dataset_tag+"-"+nxpar_rekeyed[0]] = nxpar_rekeyed[1]
            
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
    import asg_instrument

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

    som.attr_list.instrument = asg_instrument.ASG_Instrument()

    som.setAllAxisLabels(axis_labels)
    som.setAllAxisUnits(axis_units)
    som.setYLabel("Counts")
    som.setYUnits("a.u.")
    som.append(so1)

    print "SOM:",som
    print "Title:",som.getTitle()
    print "Primary Axes:",som.getAllAxisLabels(),som.getAllAxisUnits()

    som2 = SOM()
    som2.setTitle("Test SOM")
    som2.setDataSetType("histogram")
    
    so2 = so.SO(withVar=True)
    so2.axis[0].val.extend([1.0,2.0,3.0])
    so2.axis[0].var.extend([1.0,2.0,3.0])
    so2.y.extend([40.0,55.0])
    so2.var_y.extend([40.0,55.0])
    so2.id="Pixel 1"

    axis_labels = ["Extent"]
    axis_units = ["centimeters"]

    som2.attr_list.instrument = asg_instrument.ASG_Instrument()
    som2.attr_list.instrument.set_primary((15.1,0.1))

    som2.setAllAxisLabels(axis_labels)
    som2.setAllAxisUnits(axis_units)
    som2.setYLabel("Counts")
    som2.setYUnits("a.u.")
    som2.append(so2)

    if som != som2:
        print "SOMs not equal"
    else:
        print "SOMs equal"
