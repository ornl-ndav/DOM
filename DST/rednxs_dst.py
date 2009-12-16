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
import nxs
import numpy
import SOM

class RedNxsDST(dst_base.DST_BASE):
    """
    This class creates a HDF5-based reduced
    U{NeXus<http://www.nexusformat.org>} file.

    @cvar MIME_TYPE: The MIME-TYPE of the class
    @type MIME_TYPE: C{string}

    @cvar INT_TYPE: The integer type needed for NeXus file attributes
    @type INT_TYPE: C{string}

    @ivar __file: The handle to the output data file
    @type __file: C{file}
    """

    MIME_TYPE = "application/x-RedNxs"
    INT_TYPE  = 'int32'

    ########## DST_BASE functions

    def __init__(self, resource, *args, **kwargs):
        """
        Object constructor

        @param resource: The handle to the input NeXus geometry file
        @type resource: C{file}

        @param args: Argument objects that the class accepts (UNUSED)

        @param kwargs: A list of keyword arguments that the class accepts:
        """
        self.__file = nxs.open(resource, nxs.napi.ACC_CREATE5)

    def release_resource(self):
        """
        This method closes the file handle to the output file.
        """
        self.__file.close()

    def writeSOM(self, som, **kwargs):
        """
        This method writes the information contained in the given L{SOM.SOM} to
        the NeXus file.

        @param som: The object containing the information to be written.
        @type som: L{SOM.SOM}

        @param kwargs: A list of keyword arguments that the class accepts:

        @keyword entry_name: A name for the main entry in the file.
        @type entry_name: C{string}
        """
        entry_name = kwargs.get("entry_name", "entry")
        
        self.__file.makegroup(entry_name, "NXentry")
        self.__file.opengroup(entry_name, "NXentry")

        (ylabel, axislabels) = self.__sanitize_labels(som.getYLabel(),
                                                      som.getAllAxisLabels())

        for so in som:
            self.writeSO(so, ylabel, som.getYUnits(), axislabels,
                         som.getAllAxisUnits())

        # entry closing
        self.__file.closegroup() 

    def writeSO(self, so, ylabel="", yunits="", xlabels=[""], xunits=[""]):
        """
        Method to write the L{SOM.SO} information to the resource.

        @param so: The spectrum object to write to the file.
        @type so: L{SOM.SO}

        @param ylabel: The label for the dependent axis.
        @type ylabel: C{string}

        @param yunits: The units for the dependent axis.
        @type yunits: C{string}

        @param xlabels: The label for the independent axi(e)s.
        @type xlabels: C{list} of C{string}(s)

        @param xunits: The units for the independent axi(e)s.
        @type xunits: C{list} of C{string}(s)
        """
        group_name = SOM.NeXusId(so.id[0],
                                 so.id[1][0], so.id[1][1]).toJoinedStr()
        
        self.__file.makegroup(group_name, "NXdata")
        self.__file.opengroup(group_name, "NXdata")

        # Get the data dimensions
        ddims = []
        adims = []
        for axis in so.axis:
            adims.append(len(axis.val))
            # Need data lengths NOT axis lengths
            ddims.append(len(axis.val) - 1)

        # Reshape the main data
        if so.dim() > 1:
            y = so.y.toNumPy().reshape(tuple(ddims))
            var_y = numpy.sqrt(so.var_y.toNumPy()).reshape(tuple(ddims))
        else:
            y = so.y.toNumPy()
            var_y = numpy.sqrt(so.var_y.toNumPy())
        
        # Set the data and error blocks
        self.__file.makedata("data", str(y.dtype), ddims)
        self.__file.opendata("data")
        self.__file.putdata(y)
        self.__file.putattr("signal", 1, self.INT_TYPE)
        self.__file.putattr("units", yunits)
        self.__file.closedata()

        self.__file.makedata("errors", str(var_y.dtype), ddims)
        self.__file.opendata("errors")
        self.__file.putdata(var_y)
        #self.__file.putattr("signal", 1, self.INT_TYPE)
        #self.__file.putattr("units", yunits)
        self.__file.closedata()        

        for i, axis in enumerate(so.axis):
            x = axis.val.toNumPy()
            self.__file.makedata(xlabels[i], str(x.dtype), adims[i:i+1])
            self.__file.opendata(xlabels[i])
            self.__file.putdata(x)
            self.__file.putattr("primary", 1, self.INT_TYPE)
            self.__file.putattr("axis", i+1, self.INT_TYPE)
            self.__file.putattr("units", xunits[i])
            self.__file.closedata()

        # NXdata closing
        self.__file.closegroup()

    def __sanitize_labels(self, ylab, alab):
        """
        This method takes the incoming labels and replaces multiple spaces
        with and underscore and make characters all lower case.

        @param ylab: The dependent axis label to be modified.
        @type ylab: C{string}

        @param alab: The independent axi(e)s label(s) to be modified.
        @type alab: C{list} of C{strings}


        @return: The modified labels.
        @rtype: C{tuple}
        """
        import re
        ms = re.compile(r'\s+')

        alab_mod = []
        for label in alab:
            alab_mod.append(ms.sub('_', label).lower())

        return (ms.sub('_', ylab).lower(), alab_mod)

    ##### Methods not implemented
    # ----- inspection
    def get_SO_ids(self, som_id):
        """
        Method to get L{SOM.SO} IDs. 
        """
        raise NotImplementedError

    def get_SOM_ids(self):
        """
        Method to get L{SOM.SOM} IDs. 
        """
        raise NotImplementedError

    # ----- read information
    def getSO(self, som_id, so_id):
        """
        Retrieve a L{SOM.SO} from given L{SOM.SOM} and L{SOM.SO} IDs.        
        """
        raise NotImplementedError

    def getSOM(self, som_id):
        """
        Retrieve a L{SOM.SOM} for a given L{SOM.SOM} ID.
        """
        raise NotImplementedError

