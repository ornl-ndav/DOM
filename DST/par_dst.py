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
import math

class ParDST(dst_base.DST_BASE):
    """
    This class creates a so-called PAR file for TobyFit. The first row in the
    file is the total number of pixels present in the output file. Each pixel
    is then given a separate line in the file. The angles specified below
    should be in I{degrees}. The columns are arranged with the following
    information:
      1. Secondary Flight Path (L2)
      2. Polar angle (AKA TwoTheta)
      3. Azimuthal angle
      4. Detector Pixel Width (meters)
      5. Detector Pixel Height (meters)

    @cvar MIME_TYPE: The MIME-TYPE of the class
    @type MIME_TYPE: C{string}
    
    @cvar EMPTY: Variable for holding an empty string
    @type EMPTY: C{string}
    
    @cvar SPACE: Variable for holding a space
    @type SPACE: C{string}
    """

    MIME_TYPE = "text/PAR"
    EMPTY = ""
    SPACE = " "

    ########## DST_BASE functions

    def __init__(self, resource, *args, **kwargs):
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

    def writeSOM(self, som, **kwargs):
        """
        This method writes the L{SOM.SOM} information to the output file.

        @param som: The object to have its information written to file.
        @type som: L{SOM.SOM}

        @param kwargs: A list of keyword arguments that the method accepts:
        """
        # Write the total number of pixels to the file
        print >> self.__file, len(som)
        for so in som:
            self.writeData(so, som.attr_list.instrument)
                           
    ########## Call inherited functions

    def getSOM(self, som_id):
        super(dst_base.DST_BASE, self).getSOM(som_id)

    def get_SOM_ids(self):
        super(dst_base.DST_BASE, self).get_SOM_ids()        

    def getSO(self, som_id, so_id):
        super(dst_base.DST_BASE, self).getSO(som_id, so_id)

    def get_SO_ids(self, som_id):
        super(dst_base.DST_BASE, self).get_SO_ids(som_id) 

    def writeSO(self, so):
        super(dst_base.DST_BASE, self).writeSO(so)

    ############# Special functions

    def __convert_to_deg(self, angle):
        """
        This method converts an angle from radians to degrees.

        @param angle: The angle to be converted
        @type angle: C{float}


        @return: The converted angle
        @rtype: C{float}
        """
        return (180.0 / math.pi) * angle

    def __get_widths(self, sid, inst):
        """
        This method calculates the width and height of a given pixel 

        @param sid: The ID of the spectrum object
        @type sid: C{tuple}

        @param inst: The object containing the geometrical information
        @type inst: L{SOM.Instrument} or L{SOM.CompositeInstrument}        
        """
        # Get x pixel size
        x1 = inst.get_x_pix_offset(sid)

        # Make the neighboring pixel ID in the x direction
        try:
            nid = (sid[0], (sid[1][0]+1, sid[1][1]))
            x2 = inst.get_x_pix_offset(nid)
        except IndexError:
            nid = (sid[0], (sid[1][0]-1, sid[1][1]))
            x2 = inst.get_x_pix_offset(nid)
            
        # Pixel offsets are in meters
        xdiff = math.fabs(x2 - x1)

        # Get y pixel size
        y1 = inst.get_y_pix_offset(sid)        

        # Make the neighboring pixel ID in the y direction
        try:
            nid = (sid[0], (sid[1][0], sid[1][1]+1))
            y2 = inst.get_y_pix_offset(nid)
        except IndexError:
            nid = (sid[0], (sid[1][0], sid[1][1]-1))
            y2 = inst.get_y_pix_offset(nid)
            
        # Pixel offsets are in meters
        ydiff = math.fabs(y2 - y1)

        return (xdiff, ydiff)

    def writeData(self, so, inst):
        """
        This method is responsible for writing the actual data contained within
        the L{SOM.SO}s to the attached file. 

        @param so: Object containing data to be written to file
        @type so: L{SOM.SO}

        @param inst: The object containing the geometrical information
        @type inst: L{SOM.Instrument} or L{SOM.CompositeInstrument}
        """
        formatStr="%0.3f\t%0.3f\t%0.3f\t%0.3f\t%0.3f"
    
        polar = self.__convert_to_deg(inst.get_polar(so.id)[0])
        azi = self.__convert_to_deg(inst.get_azimuthal(so.id)[0])

        (dw, dh) = self.__get_widths(so.id, inst)

        print >> self.__file, formatStr % (inst.get_secondary(so.id)[0],
                                           polar, azi, dw, dh)
                                           
