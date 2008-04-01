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
    """
    This class is the container for scientific data and metadata. The data is
    contained by L{SO}s within a C{SOM}s internal list. Metadata is held in
    an extensible L{AttributeList}. Instrument geometry information is kept in
    either a L{CompositeInstrument} or an L{Instrument} object. Sample
    information is kept in a L{Sample} object.

    @cvar EMPTY: Variable for holding an empty string
    @type EMPTY: C{string}

    @ivar __title__: Dataset description
    @type __title__: C{string}

    @ivar __axis_labels__: Labels for the independent axes
    @type __axis_labels__: C{list} of C{string}s

    @ivar __axis_units__: Units for the independent axes
    @type __axis_units__: C{list} of C{string}s

    @ivar __y_label__: The label for the dependent axis
    @type __y_label__: C{string}

    @ivar __y_units__: The units for the dependent axis
    @type __y_units__: C{string}

    @ivar __data_set_type__: The axis type of the associated data. The values
                             are I{histogram}, I{coordinate} or I{density}.
                             The last two are describing the same type of data.
    @type __data_set_type__: C{string}

    @ivar attr_list: The dictionary of metadata for the dataset
    @type attr_list: L{AttributeList}

    @ivar dst: The pointer to the file containing the data for the dataset.
               B{NOTE}: This is currently unused.
    @type dst: L{DST}
    """
    
    EMPTY = ""

    def __init__(self):
        """
        Object constructor
        """
        self.__title__ = SOM.EMPTY
        self.__axis_labels__ = []
        self.__axis_units__ = []
        self.__y_label__ = SOM.EMPTY
        self.__y_units__ = SOM.EMPTY
        self.__data_set_type__ = SOM.EMPTY
        
        self.attr_list = attribute.AttributeList()
        self.dst = None

    def __eq__(self, other):
        """
        This method checks to see if the incoming C{SOM} object and the
        current one are equal.

        @param other: Object to check for equality
        @type other: C{SOM}


        @return: I{True} if the C{SOM} objects are equal, I{False} if they
                 are not
        @rtype: C{boolean}
        """
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
        """
        This method checks to see if the incoming C{SOM} object and the
        current one are not equal.

        @param other: Object to check for equality
        @type other: C{SOM}


        @return: I{True} if the C{SOM} objects are not equal, I{False} if they
                 are
        @rtype: C{boolean}
        """
        return not self.__eq__(other)
        
    def copyAttributes(self, other, add_nxpars=False):
        """
        This method copies attributes from another C{SOM}. If parameters need
        to be added, a flag is used to obtain this behavior.

        @param other: Object to copy attributes from
        @type other: C{SOM}

        @param add_nxpars: Flag for using addition feature on L{NxParameter}s.
                           The default value is I{False}.
        @type add_nxpars: C{boolean}
        """
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
                nxpar_keys = [item[0] for item in self.attr_list.iteritems() \
                              if isinstance(item[1], NxParameter)]

                for nxpar_key in nxpar_keys:
                    self.attr_list[nxpar_key] += other.attr_list[nxpar_key]
            else:
                # Do nothing
                pass
                    
            keys_to_get = [other_key for other_key in other.attr_list \
                           if other_key not in self.attr_list]
                
            for key_to_get in keys_to_get:
                self.attr_list[key_to_get] = \
                                       copy.copy(other.attr_list[key_to_get])

    def axisUnitsAt(self, units):
        """
        This method returns the axis index (starting from zero) according to
        the units requested.

        @param units: The units to search for in the independent axes.
        @type units: C{string}


        @return: The index of the independent axis with the requested units. If
                 more than one axis has the same units, the first one found
                 will be returned.
        @rtype: C{int}
        """
        return self.__axis_units__.index(units)
    
    def getAllAxisLabels(self):
        """
        This method returns all of the independent axis labels.

        @return: The labels of the independent axes
        @rtype: C{list} of C{string}s
        """
        import copy
        return copy.copy(self.__axis_labels__)

    def getAllAxisUnits(self):
        """
        This method returns all of the independent axis units.

        @return: The units of the independent axes
        @rtype: C{list} of C{string}s
        """
        import copy
        return copy.copy(self.__axis_units__)

    def getAxisLabel(self, dim=0):
        """
        This method returns the independent axis label at the requested index.

        @param dim: The index to request the independent axis label.
        @type dim: C{int}

        @return: The label of the independent axis at the requested index
        @rtype: C{string}
        """
        return self.__axis_labels__[dim]
    
    def getAxisUnits(self, dim=0):
        """
        This method returns the independent axis units at the requested index.

        @param dim: The index to request the independent axis units.
        @type dim: C{int}

        @return: The units of the independent axis at the requested index
        @rtype: C{string}
        """        
        return self.__axis_units__[dim]

    def getDataSetType(self):
        """
        This method returns the dataset type of this C{SOM}.

        @return: The dataset type
        @rtype: C{string}
        """
        return self.__data_set_type__

    def getDimension(self):
        """
        This method returns the number of independent axes in the C{SOM}.

        @return: The number of independent axes
        @rtype: C{int}
        """
        return len(self.__axis_labels__)

    def getTitle(self):
        """
        This method returns the title associated with the dataset.

        @return: The title of the dataset
        @rtype: C{string}
        """
        return self.__title__

    def getYLabel(self):
        """
        This method returns the dependent axis label.

        @return: The dependent axis label
        @rtype: C{string}
        """        
        return self.__y_label__

    def getYUnits(self):
        """
        This method returns the dependent axis units.

        @return: The dependent axis units
        @rtype: C{string}
        """                
        return self.__y_units__

    def hasAxisUnits(self, unit):
        """
        This function checks the array of primary axes for the requested units.
        If there are duplicate units, it will always find the first.
        
        @param unit: The name of the units to be searched for
        @type unit: C{string}
        

        @return: A determination if the units exist
        @rtype: C{boolean}
        """
        return self.__axis_units__.__contains__(unit)

    def rekeyNxPars(self, dataset_tag):
        """
        This function prepends a dataset tag to the keys of L{NxParameter}s in
        the L{SOM}s attribute list.

        @param dataset_tag: The name to prepend to the key
        @type dataset_tag: C{string}
        """
        nxpar_keys = [item[0] for item in self.attr_list.iteritems() \
                      if isinstance(item[1], NxParameter)]
        
        nxpar_values = []
        for nxpar_key in nxpar_keys:
            nxpar_values.append(self.attr_list.pop(nxpar_key))

        import itertools
        for nxpar_rekeyed in itertools.izip(nxpar_keys, nxpar_values):
            self.attr_list[dataset_tag+"-"+nxpar_rekeyed[0]] = nxpar_rekeyed[1]
            
    def setAllAxisLabels(self, labels):
        """
        This method sets all of the labels for the independent axes.

        @param labels: The labels for all of the independent axes
        @type labels: C{list} of C{string}s
        """
        self.__axis_labels__ = labels

    def setAllAxisUnits(self,units):
        """
        This method sets all of the units for the independent axes.

        @param units: The units for all of the independent axes
        @type units: C{list} of C{string}s
        """        
        self.__axis_units__ = units

    def setAxisLabel(self, dim, label):
        """
        This method sets the label for the independent axis at the requested
        index.

        @param dim: The index to request the independent axis label.
        @type dim: C{int}
        
        @param label: The label for the independent axis
        @type label: C{string}
        """        
        try:
            self.__axis_labels__[dim] = label
        except IndexError:
            self.__axis_labels__.append(label)            
    
    def setAxisUnits(self, dim, units):
        """
        This method sets the units for the independent axis at the requested
        index.

        @param dim: The index to request the independent axis units.
        @type dim: C{int}
        
        @param units: The units for the independent axis
        @type units: C{string}
        """        
        try:
            self.__axis_units__[dim] = units
        except IndexError:
            self.__axis_units__.append(units)            

    def setDataSetType(self, type):
        """
        This method sets the dataset type for the C{SOM}.

        @param type: The name of the dataset type for the associated data.
                     The accepted values are I{histogram}, I{density} and
                     I{coordinate}.
        @type type: C{string}
        """
        self.__data_set_type__ = type

    def setTitle(self, title):
        """
        This method sets the title for the associated data in the C{SOM}.

        @param title: The title for the data
        @type title: C{string}
        """
        self.__title__ = title

    def setYLabel(self, label):
        """
        This method sets the label for the dependent axis.

        @param label: The label for the dependent axis
        @type label: C{string}
        """
        self.__y_label__ = label

    def setYUnits(self, units):
        """
        This method sets the units for the dependent axis.

        @param units: The units for the dependent axis
        @type units: C{string}
        """        
        self.__y_units__ = units

    def toXY(self, **kwargs):
        """
        This method returns the data encapsulated in the L{SOM.SO}s as a set
        of lists. The positioning of the information goes as follows:
        I{[(x1_1, sx1_1, x2_1, sx2_1, ... , y_1, sy_1), (x1_2, sx1_2, x2_2,
        sx2_2, ... , y_2, sy_2) ...]. The variances are controlled by keywords
        and do not appear in the returned tuples by default. For
        multidimensional data, the y and sy arrays have the size of the
        multiplication of the individual axis sizes (axis size - 1 for
        histogram data). If variances are requested but are not filled in the
        respective L{SOM.SO}s, the I{None} type will be placed in the
        appropriate location within the tuple.

        @param kwargs: A list of keyword arguments that the function accepts

        @keyword withXvar: A flag that will add the x-axis variances to the
                           output tuple.
        @type withXvar: C{boolean}

        @keyword withYvar: A flag that will add the y-axis variance to the
                           output tuple.
        @type withYvar: C{boolean}
        """
        try:
            withXvar = kwargs["withXvar"]
        except KeyError:
            withXvar = False
        
        try:
            withYvar = kwargs["withYvar"]
        except KeyError:
            withYvar = False
            
        arrays = []

        for so in self:
            info = []
            for i in range(len(so.axis)):
                info.append(so.axis[i].val[:])
                if withXvar:
                    info.append(so.axis[i].var[:])
            info.append(so.y[:])
            if withYvar:
                info.append(so.var_y[:])
            arrays.append(tuple(info))

        return arrays
        
if __name__ == "__main__":
    import so
    import asg_instrument

    som = SOM()
    som.setTitle("Test SOM")
    som.setDataSetType("histogram")
    
    so1 = so.SO(withVar=True, construct=True)
    so1.axis[0].val.extend([1.0,2.0,3.0])
    so1.axis[0].var.extend([1.0,2.0,3.0])
    so1.y.extend([40.0,55.0])
    so1.var_y.extend([40.0,55.0])
    so1.id = "Pixel 1"

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
    
    so2 = so.SO(withVar=True, construct=True)
    so2.axis[0].val.extend([1.0,2.0,3.0])
    so2.axis[0].var.extend([1.0,2.0,3.0])
    so2.y.extend([40.0,55.0])
    so2.var_y.extend([40.0,55.0])
    so2.id = "Pixel 1"

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

    print "SOM1:", som.toXY(withXvar=True)
    print "SOM2:", som2.toXY(withYvar=True)
