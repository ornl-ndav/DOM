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

import dst_base
import dst_utils
import math
import SOM

class Dave2dDST(dst_base.DST_BASE):
    """
    This class creates a DAVE 2D ASCII file with a metadata footer. The
    formatting is based on what is found
    U{here<http://www.ncnr.nist.gov/dave/documentation/ascii_help.pdf>}.
    
    @cvar MIME_TYPE: The MIME-TYPE of the class
    @type MIME_TYPE: C{string}
    
    @cvar EMPTY: Variable for holding an empty string
    @type EMPTY: C{string}
    
    @cvar SPACE: Variable for holding a space
    @type SPACE: C{string}

    @ivar __file: The handle to the output data file
    @type __file: C{file}

    @ivar __epoch: The epoch (UNIX time) when the object was instantiated.
                   This is used as the creation time of the file information.
    @type __epoch: C{string}

    @ivar __nx: The number of x axis (slowest running) elements. This is used
                during file read in.
    @type __nx: C{int}

    @ivar __ny: The number of y axis (slowest running) elements. This is used
                during file read in.
    @type __ny: C{int}

    @ivar __axis_info: This is used to store the axis label and unit
                       information across internal function calls. This is
                       used during file read in.
    @type __axis_info: C{list} of C{string}s

    @ivar __axis_ok: This is used to store the flag determining if the
                     incoming axis information should be written as is. This
                     is used during file write out.
    @type __axis_ok: C{boolean}
    """
    
    MIME_TYPE = "text/Dave2d"
    EMPTY = ""
    SPACE = " "

    ########## DST_BASE functions

    def __init__(self, resource, *args, **kwargs):
        """
        Object constructor

        @param resource: The handle to the output data file
        @type resource: C{file}

        @param args: Argument objects that the class accepts (UNUSED)

        @param kwargs: A list of keyword arguments that the class accepts:

        @keyword axis_ok: A flag that lets the instance know that the incoming
                          axis information should be taken as is. This is only
                          used during write-out. The default value is I{False}.
        @type axis_ok: C{boolean}
        """        
        import time
        
        self.__file = resource
        self.__epoch = time.time()
        try:
            self.__axis_ok = kwargs["axis_ok"]
        except KeyError:
            self.__axis_ok = False

    def release_resource(self):
        """
        This method closes the file handle to the output file.
        """        
        self.__file.close()

    def getSOM(self, som_id=None):
        """
        This method parses the resource and creates a SOM from the information.

        @param som_id: The name of the SOM. The default value is C{None}. This
        retrieves all information. 
        """
        som = SOM.SOM()
        som.setDataSetType("density")

        self.__set_axes(som)
        self.__readData(som)

        som.setYLabel("Counts")
        uscale = som.getAxisUnits(1) + " " + som.getAxisUnits(0)
        som.setYUnits("Counts / " + uscale)

        som.attr_list = dst_utils.parse_spec_header(self.__file)

        return som

    def writeSO(self, so):
        """
        This method writes the L{SOM.SO} information to the output file.

        @param so: The object to have its information written to file.
        @type so: L{SOM.SO}
        """        
        self.writeData(so)

    def writeSOM(self, som):
        """
        This method writes the L{SOM.SOM} information to the output file. The
        C{SOM.SOM} carries only one C{SOM.SO} that has a 2-dimensional spectrum
        contained in it.

        @param som: The object to have its information written to file.
        @type som: L{SOM.SOM}
        """
        self.writeXValues(som)
        self.writeData(som[0])
        dst_utils.write_spec_header(self.__file, self.__epoch, som)

    ########## Special functions

    def writeXValues(self, som):
        """
        This method is responsible for writing the values of the two
        independent axes to the file. The values must be converted to bin
        centers.
        
        @param som: The object containing the information about the independent
                    axes.
        @type som: L{SOM.SOM}
        """
        so = som[0]
        if self.__axis_ok:
            len_x1 = len(so.axis[1].val)
            len_x2 = len(so.axis[0].val)
        else:
            len_x1 = len(so.axis[1].val) - 1
            len_x2 = len(so.axis[0].val) - 1
            
        print >> self.__file, "# Number of", som.getAxisLabel(1), "values"
        print >> self.__file, len_x1
        print >> self.__file, "# Number of", som.getAxisLabel(0), "values"
        print >> self.__file, len_x2

        fast_axis = "# %s (%s) Values:" % (som.getAxisLabel(1),
                                           som.getAxisUnits(1))

        print >> self.__file, fast_axis
        for i in range(len_x1):
            if self.__axis_ok:
                print >> self.__file, so.axis[1].val[i]
            else:
                print >> self.__file, so.axis[1].val[i] + \
                      (so.axis[1].val[i+1] - so.axis[1].val[i]) / 2.0

        slow_axis = "# %s (%s) Values:" % (som.getAxisLabel(0),
                                           som.getAxisUnits(0))

        print >> self.__file, slow_axis
        for i in range(len_x2):
            if self.__axis_ok:
                print >> self.__file, so.axis[0].val[i]
            else:
                print >> self.__file, so.axis[0].val[i] + \
                      (so.axis[0].val[i+1] - so.axis[0].val[i]) / 2.0
        
    def writeData(self, so):
        """
        This method is responsible for writing the actual data contained within
        the L{SOM.SO}s to the attached file. 

        @param so: Object containing data to be written to file
        @type so: L{SOM.SO}
        """
        if self.__axis_ok:
            len_x1 = len(so.axis[0].val)
            len_x2 = len(so.axis[1].val)
        else:
            len_x1 = len(so.axis[0].val) - 1
            len_x2 = len(so.axis[1].val) - 1

        for i in range(len_x1):
            print >> self.__file, "# Group", i
            slice_y = so.y[i*len_x2:((i+1)*len_x2)]
            slice_var_y = so.var_y[i*len_x2:((i+1)*len_x2)] 

            for (y, var_y) in map(None, slice_y, slice_var_y):
                print >> self.__file, y, self.SPACE, \
                      math.sqrt(math.fabs(var_y))

    def __create_axis(self, axis, som):
        """
        This method fills in the axis values for a given axis and it also
        retrieves the label and unit information as well.

        @param axis: The particular axis to set the values for. The values for
                     this parameter are I{x} or I{y}.
        @type axis: C{string}
        
        @param som: The object to have its information read from file.
        @type som: L{SOM.SOM}
        """
        import os

        # Add label and unit information for axis
        lline = self.__file.readline().rstrip(os.linesep)
        self.__axis_info.append(self.__get_label_units(lline))
        
        if axis == "x":
            num_vals = self.__nx
            axis_index = 0
        else:
            num_vals = self.__ny
            axis_index = 1

        # Set the axis values
        for i in xrange(num_vals):
            line = self.__file.readline().rstrip(os.linesep)
            som[0].axis[axis_index].val.append(float(line))

    def __get_label_units(self, lline):
        """
        This method strips out the axis label and units from the provided
        information.

        @param lline: The object containing the label and unit information.
        @type lline: C{string}


        @return: The axis label and units
        @rtype: C{tuple} of two C{string}s
        """
        parts = lline.split()

        # The units sit at -2 in the list
        return (" ".join(parts[1:-2]), dst_utils.units_from_string(parts[-2]))
            
    def __readData(self, som):
        """
        This method reads through the data adding the counts and associated
        squared errors.

        @param som: The object to have its information read from file.
        @type som: L{SOM.SOM}
        """
        import os
        for i in xrange(self.__nx):
            for j in xrange(self.__ny):
                # Skip the Group tag
                if j == 0:
                    lline = self.__file.readline()
                    
                lline = self.__file.readline().rstrip(os.linesep)
                parts = lline.split()

                som[0].y.append(float(parts[0]))
                som[0].var_y.append(float(parts[1]) * float(parts[1]))
                
    def __set_axes(self, som):
        """
        This method sets up the x and y axes for the spectrum object

        @param som: The object to have its information read from file.
        @type som: L{SOM.SOM}
        """
        import os
        # Need the top four lines of the file to get the number of axis
        # elements
        for i in xrange(4):
            line = self.__file.readline().rstrip(os.linesep)
            if i == 1:
                self.__ny = int(line)
            elif i == 3:
                self.__nx = int(line)

        self.__axis_info = []

        so = SOM.SO(id=0, dim=2, construct=True)
        som.append(so)

        # Y axis is fastest runner, so do it first
        self.__create_axis("y", som)
        self.__create_axis("x", som)

        # Get the x and y axis label and units
        som.setAllAxisLabels([self.__axis_info[1][0], self.__axis_info[0][0]])
        som.setAllAxisUnits([self.__axis_info[1][1], self.__axis_info[0][1]])

        
