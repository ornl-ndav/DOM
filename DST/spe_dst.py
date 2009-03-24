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

class SpeDST(dst_base.DST_BASE):
    """
    This class creates a SPE ASCII file.
    """
    
    MIME_TYPE = "text/SPE"
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

        @keyword comments: Comments to add to the file header.
        @type comments: C{list} of C{string}s        
        """        
        import time
        
        self.__file = resource
        self.__epoch = time.time()
        try:
            self.__axis_ok = kwargs["axis_ok"]
        except KeyError:
            self.__axis_ok = False

        try:
            self.__comments = kwargs["comments"]
        except KeyError:
            self.__comments = None

    def release_resource(self):
        """
        This method closes the file handle to the output file.
        """        
        self.__file.close()

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
        for so in som:
		self.writeData(so)
        #dst_utils.write_spec_header(self.__file, self.__epoch, som,
        #                            comments=self.__comments)

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
        
	len_det = len(som)
        len_energy = len(so.axis[0].val)
        
        print >> self.__file, len_det, len_energy-1

        print >> self.__file, "### Phi Grid"
	for i in range(len_det+1):
	    print >> self.__file, " %10.3e" % ((i*0.5)+0.5),
	    if ((i+1) % 8) == 0:
		print >> self.__file

	# Make sure that there is a newline at the end of this section
	if ((len_det+1) % 8) != 0:
		print >> self.__file

        print >> self.__file, "### Energy Grid"
        for i in range(len_energy):
            print >> self.__file, " %10.3e" % (so.axis[0].val[i]),  
	    if ((i+1) % 8) == 0:
		print >> self.__file
	    
	# Make sure that there is a newline at the end of this section
	if ((len_energy) % 8) != 0:
		print >> self.__file
        
    def writeData(self, so):
        """
        This method is responsible for writing the actual data contained within
        the L{SOM.SO}s to the attached file. 

        @param so: Object containing data to be written to file
        @type so: L{SOM.SO}
        """
        len_x1 = len(so.axis[0].val)


        for i in range(len_x1):
            print >> self.__file, "### S(Phi,w)"
	    counter_y=1
	    for y in so.y:	
	        print >> self.__file, " %10.3e" % (y),
		if (counter_y % 8) == 0:
			print >> self.__file
                counter_y=counter_y+1

	    # Make sure that there is a newline at the end of this section
	    # (we subtract the 1 because we've just added it at the end of 
	    # the above loop!
	    if ((counter_y-1) % 8) != 0:
		print >> self.__file

            print >> self.__file, "### Errors"
	    counter_var_y = 1
	    for var_y in so.var_y:
	        print >> self.__file, " %10.3e" % (math.sqrt(math.fabs(var_y))),
		if (counter_var_y % 8) == 0:
			print >> self.__file
		counter_var_y = counter_var_y + 1
	    
	    # Make sure that there is a newline at the end of this section
	    # (we subtract the 1 because we've just added it at the end of 
	    # the above loop!
	    if ((counter_var_y-1) % 8) != 0:
		print >> self.__file

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
                if self.__no_sqr__:
                    som[0].var_y.append(float(parts[1]))
                else:
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

        
