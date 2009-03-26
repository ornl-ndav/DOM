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
    
    The first line contains the number of angle and energy bins.
    Then the angle bin boundaries are listed (not used so are nonsense).
    The the energy bin bounaries are listed.
    
    Then for each angle, the grid of energy/error values are listed
    
    The format for the grids is 8E10.3 (fortran) or 8 values of %10.3e per line. 
    
    @cvar MIME_TYPE: The MIME-TYPE of the class
    @type MIME_TYPE: C{string}
    
    @cvar EMPTY: Variable for holding an empty string
    @type EMPTY: C{string}
    
    @cvar SPACE: Variable for holding a space
    @type SPACE: C{string}
    """
    
    MIME_TYPE = "text/SPE"
    EMPTY = ""
    SPACE = " "

    ########## DST_BASE functions

    def __init__(self, resource):
        """
        Object constructor

        @param resource: The handle to the output data file
        @type resource: C{file}
        """
        self.__file = resource

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
	    print >> self.__file, "%10.3f" % 1.0,
	    if ((i+1) % 8) == 0:
		print >> self.__file

	# Make sure that there is a newline at the end of this section
	if ((len_det+1) % 8) != 0:
		print >> self.__file

        print >> self.__file, "### Energy Grid"
        for i in range(len_energy):
            print >> self.__file, "%10.3e" % (so.axis[0].val[i]),  
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

	print >> self.__file, "### S(Phi,w)"
	counter_y=1
	for y in so.y:	
	    print >> self.__file, "%10.3e" % (y),
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
	    print >> self.__file, "%10.3e" % (math.sqrt(math.fabs(var_y))),
	    if (counter_var_y % 8) == 0:
		    print >> self.__file
	    counter_var_y = counter_var_y + 1
	
	# Make sure that there is a newline at the end of this section
	# (we subtract the 1 because we've just added it at the end of 
	# the above loop!
	if ((counter_var_y-1) % 8) != 0:
	    print >> self.__file


