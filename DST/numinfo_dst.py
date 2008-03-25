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

class NumInfoDST(dst_base.DST_BASE):
    """
    This class writes a 3 column ASCII file based on the
    U{spec<http://www.certif.com/spec_manual/user_1_4_1.html>} file format.
    The columns in this case are restricted to a pixel ID, a value and its
    associated uncertainty.

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

    @ivar __tag: The label for the values being written to file.
    @type __tag: C{string}

    @ivar __units: The units for the values being written to file.
    @type __units: C{string}

    @ivar __comments: Comments to add to the file header.
    @type __comments: C{list} of C{string}s
    """
    
    MIME_TYPE = "text/num-info"
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

        @keyword tag: The label for the values being written to file. The
                      default is I{Integral}.
        @type tag: C{string}
        
        @keyword units: The units for the values being written to file. The
                        default is I{counts}.
        @type units: C{string}
        
        @keyword comments: Comments to add to the file header.
        @type comments: C{list} of C{string}s
        """        
        import time

        self.__file = resource
        self.__epoch = time.time()

        try:
            self.__tag = kwargs["tag"]
        except KeyError:
            self.__tag = "Integral"

        try:
            self.__units = kwargs["units"]
        except KeyError:
            self.__units = "counts"

        try:
            self.__comments = kwargs["comments"]
        except KeyError:
            self.__comments = None
        
    def release_resource(self):
        """
        This method closes the file handle to the output file.
        """                
        self.__file.close()

    def getSOM(self, som_id=None, **kwargs):
        """
        This method parses the resource and creates a SOM from the information.

        @param som_id: The name of the SOM. The default value is C{None}. This
                       retrieves all information. If multiple detector IDs are
                       specified, they should be comma-separated.
        @type som_id: C{string}

        @param kwargs: A list of keyword arguments that the function accepts:

        @keyword roi_file: A list of spectrum IDs to filter the data on
        @type roi_file: C{string}
        """
        # Check for list of detector IDs
        if som_id is not None:
            if "," in som_id:
                som_ids = som_id.split(',')
            else:
                som_ids = [som_id]
        # Check to see if an ROI file was passed
        try:
            roi_filename = kwargs["roi_file"]
            try:
                roi = SOM.Roi(roi_filename)
            except TypeError:
                # roi_filename is None
                roi = None
        except KeyError:
            roi = None
        
        som = SOM.SOM()

        som.attr_list = dst_utils.parse_spec_header(self.__file)

        # Reset file read to not miss #L line
        fname = self.__file.name
        self.release_resource
        self.__file = open(fname, "r")

        for line in self.__file:
            if line.startswith("#L"):
                self.readSOM(som, line)
            elif line.startswith("("):
                lparts = line.split()
                # The spectrum ID is the first three slots
                so_id = SOM.NeXusId.fromList(lparts[0:3])

                filter_so = False
                # Check the list of detector IDs
                if som_id is not None:
                    if so_id.getDetId() not in som_ids:
                        filter_so = True

                # Check the ROI list
                if roi is not None:
                    if so_id not in roi:
                        filter_so = True

                if not filter_so:
                    self.readSO(som, so_id.toTuple(), lparts)

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
        This method writes the L{SOM.SOM} information to the output file.

        @param som: The object to have its information written to file.
        @type som: L{SOM.SOM}
        """        
        dst_utils.write_spec_header(self.__file, self.__epoch, som)

        if self.__comments is not None:
            for comment in self.__comments:
                print >> self.__file, "#C", comment
 	       
        print >> self.__file, \
              "#L Pixel ID  %s (%s) Error (%s)" % (self.__tag, self.__units,
                                                   self.__units)
        for so in som:
            self.writeData(so)

    ########## Special functions

    def readSO(self, som, so_id, parts):
        """
        This method reads the data lines and creates the appropriate SOs for
        the data.

        @param som: The object to have its information set from file.
        @type som: L{SOM.SOM}

        @param so_id: The identifier for the individual spectrum
        @type so_id: C{tuple}
        
        @param parts: The object containing the data
        @type parts: C{list}
        """
        so = SOM.SO()

        # Set the spectrum ID
        so.id = so_id
        # Get the value
        so.y = float(parts[-2])
        # Need to square the error since we carry around error^2
        so.var_y = (float(parts[-1]) * float(parts[-1]))

        som.append(so)

    def readSOM(self, som, lline):
        """
        This method reads the #L line and sets up some initial information in
        the L{SOM.SOM}.

        @param som: The object to have its information read from file.
        @type som: L{SOM.SOM}

        @param lline: The line from the file containing the information to set
        @type lline: C{string}
        """
        parts = lline.split()
        # Find the units
        units = []
        count = 0
        for part in parts:
            if part.startswith("("):
                units.append(count)
            count += 1
        
        # Between thrid entry and first units is the y axis label
        label = parts[3:units[0]]
        som.setYLabel(" ".join(label))
        # Next entry after that is the y axis units
        som.setYUnits(dst_utils.units_from_string(parts[units[0]]))

    def writeData(self, so):
        """
        This method is responsible for writing the actual data contained within
        the L{SOM.SO}s to the attached file. 

        @param so: Object containing data to be written to file
        @type so: L{SOM.SO}
        """        
        try:
            variance = math.sqrt(so.var_y)
        except OverflowError:
            variance = float('inf')
        
        print >> self.__file, so.id, so.y, variance
