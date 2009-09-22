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
import nexus_dst
import nexus_file
import SOM

class GeomDST(dst_base.DST_BASE):
    """
    This class creates a NeXus geometry DST which can subsequently be passed
    into a L{SOM.SOM} with an existing geometry. The file format for the
    geometry information is based on the
    U{NeXus<http://www.nexusformat.org>} format specification.

    @cvar MIME_TYPE: The MIME-TYPE of the class
    @type MIME_TYPE: C{string}

    @ivar __nexus: The handle to the NeXus geometry file
    @type __nexus: L{nexus_file.NeXusFile}

    @ivar __tree: A list of key-value pairs from the file structure of the
                  NeXus geometry file.
    @type __tree: C{dict}

    @ivar __inst_info: Instrument geometry information
    @type __inst_info: C{dict} of C{NeXusInstrument}s

    @ivar __sns_info: Instrument information that is not geometry related
    @type __sns_info: C{dict} of C{SnsInformation}s
    """
    
    MIME_TYPE = "application/x-NxsGeom"

    def __init__(self, resource, *args, **kwargs):
        """
        Object constructor

        @param resource: The handle to the input NeXus geometry file
        @type resource: C{file}

        @param args: Argument objects that the class accepts (UNUSED)

        @param kwargs: A list of keyword arguments that the class accepts:
        """
        self.__nexus = nexus_file.NeXusFile(resource)
        self.__tree = self.__build_tree()

        self.__inst_info = nexus_dst.NeXusInstrument(self.__nexus,
                                                     self.__tree,
                                                     from_saf=True)
        self.__sns_info = nexus_dst.SnsInformation(self.__nexus, self.__tree,
                                                   self.__inst_info.getName(),
                                                   from_saf=True)

    def setGeometry(self, som_id, som):
        """
        This method reads in a geometry from the associated file and places
        that geometry into the incoming L{SOM.SOM}. This overrides the
        geometry that was currently present.

        @param som_id: The NeXus path IDs of the geometry information
        @type som_id: C{string} or C{list} of C{string}s

        @param som: The object being provided a replacement geometry
        @type som: L{SOM.SOM}
        """
        id_list = []
        try:
            som_id.reverse()
            som_id.reverse()
            for i in range(len(som_id)):
                id_list.append(som_id[i])
        except AttributeError:
            id_list.append(som_id)

        inst_keys = []

        # If there is only one ID in the list, expect that starting and
        # ending ids are a single tuple each
        if len(id_list) == 1:
            len_id_1 = True
        else:
            len_id_1 = False

        for id in id_list:
            inst_keys.append(id[0].split('/')[-1])
            inst_keys.append(self.__inst_info.getInstrument(id[0],
                                                            from_saf=True))

        if len(inst_keys) > 2:
            inst = SOM.CompositeInstrument(pairs=inst_keys)
            som.attr_list.instrument = inst
        else:
            som.attr_list.instrument = inst_keys[1]

        som.attr_list["instrument_name"] = som.attr_list.instrument.get_name()

        info_keys = self.__sns_info.getKeys()
        for key in info_keys:
            pair_list = self.__sns_info.getInformation(key)
            if pair_list[1] is None:
                info = None
            else:
                if len(pair_list) > 2:
                    info = SOM.CompositeInformation(pairs=pair_list)
                else:
                    info = pair_list[1]

            if key is not None:
                som.attr_list[key] = info

        return

    def release_resource(self):
        """
        This method closes the file handle to the output file.
        """        
        del self.__nexus
        del self.__tree
        del self.__inst_info
        del self.__sns_info

    def __list_level(self):
        """
        This method provides a listing of the directory tree structure of the
        NeXus geometry file.

        @return: The listing of the directory tree
        @rtype: C{dict}
        """
        listing = {}
        self.__nexus.initgroupdir()
        name = "blah"
        while name is not None:
            (name, type) = self.__nexus.getnextentry()
            if (name is not None) and (type != "CDF0.0"):
                listing[name] = type
        return listing

    def __prepend_parent(self, parent, listing):
        """
        This method restructures an incoming file structure listing by
        prepending the specified parent node information.

        @param parent: The parent node for prepending
        @type parent: C{atring}

        @param listing: The file directory structure listing
        @type listing: C{dict}
        """
        my_list = {}
        for key in listing:
            my_list[("%s/%s" % (parent, key))] = listing[key]
        return my_list

    def __build_tree(self, listing={}):
        """
        This method builds a path tree from the NeXus geometry file.

        @param listing: Placeholder for the file directory structure listing
        @type listing: C{dict}


        @return: The file directory structure listing
        @rtype: C{dict}
        """
        # set up result
        my_listing = listing.copy()

        # get a listing for each element in the tree
        if(listing is not None) and (len(listing) > 0):
            for parent in listing:
                if(not listing[parent] == "SDS"):
                    self.__nexus.openpath(parent)
                    level_listing = self.__list_level()
                    level_listing = self.__prepend_parent(parent,
                                                          level_listing)
                    for inner in level_listing:
                        my_listing[inner] = level_listing[inner]
        # or start at the beginning
        else:
            my_listing = self.__prepend_parent("", self.__list_level())

        # recurse if the list has changed
        if len(my_listing) > len(listing):
            return self.__build_tree(my_listing)
        else:
            return my_listing
