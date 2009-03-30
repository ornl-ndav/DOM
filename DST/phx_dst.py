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

class PhxDST(dst_base.DST_BASE):
    """
    This class creates a so-called PHX file for programs like MSlice. The first
    row in the file is the total number of pixels present in the output file.
    Each pixel is then given a separate line in the file. The angles specified
    below should be in I{degrees}. The columns are
    arranged with the following information:
      1. Historically redundant info (set to 1)
      2. Historically redundant info (set to 0)
      3. Polar angle (AKA TwoTheta)
      4. Azimuthal angle
      5. Delta polar
      6. Delta azimuthal
      7. Historically redundant info (set to 0)

    @cvar MIME_TYPE: The MIME-TYPE of the class
    @type MIME_TYPE: C{string}
    
    @cvar EMPTY: Variable for holding an empty string
    @type EMPTY: C{string}
    
    @cvar SPACE: Variable for holding a space
    @type SPACE: C{string}
    """

    MIME_TYPE = "text/PHX"
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
            self.writeData(so, som.attr_list.instrument,
                           som.attr_list["corner_geom"])

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

    def __get_widths(self, cangles):
        """
        This method calculates the widths in polar and aziumthal angles.

        @param cangles: The corner angle information for a given pixel
        @type cangles: C{hlr_utils.Angles}
        """
        pol1 = (cangles.getPolar(0) + cangles.getPolar(1)) / 2.0
        pol2 = (cangles.getPolar(2) + cangles.getPolar(3)) / 2.0
        delta_pol = self.__convert_to_deg(pol1 - pol2)

        azi1 = (cangles.getAzimuthal(0) + cangles.getAzimuthal(3)) / 2.0
        azi2 = (cangles.getAzimuthal(1) + cangles.getAzimuthal(2)) / 2.0
        delta_azi = self.__convert_to_deg(azi1 - azi2)

        return (math.fabs(delta_pol), math.fabs(delta_azi))

    def writeData(self, so, inst, cgeom):
        """
        This method is responsible for writing the actual data contained within
        the L{SOM.SO}s to the attached file. 

        @param so: Object containing data to be written to file
        @type so: L{SOM.SO}

        @param inst: The object containing the geometrical information
        @type inst: L{SOM.Instrument} or L{SOM.CompositeInstrument}

        @param cgeom: The object containing the corner angle information
        @type cgeom: C{dict}
        """
        formatStr="%d\t%d\t%0.3f\t%0.3f\t%0.3f\t%0.3f\t%d"

        dummy1 = 1
        dummy2 = 0
        dummy7 = 0
    
        polar = self.__convert_to_deg(inst.get_polar(so.id)[0])
        azi = self.__convert_to_deg(inst.get_azimuthal(so.id)[0])

        (dpolar, dazi) = self.__get_widths(cgeom[str(so.id)])

        print >> self.__file, formatStr % (dummy1, dummy2, polar, azi,
                                           dpolar, dazi, dummy7)
        
