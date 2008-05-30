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

import instrument

class CompositeInstrument(instrument.Instrument):
    """
    This class creates a collection of L{Instrument} objects. The individual
    instruments a accessed via an internal hash according to a given
    instrument key. The member function call is then passed onto the
    appropriate instrument object.

    @ivar __inst_hash: Hash table for L{Instrument} objects for different
                       banks of a full instrument.
    @type __inst_hash: C{dict}
    """
    
    def __init__(self, *args, **kwargs):
        """
        Constructor for class. Keys and instruments can be passed as a list
        of arguments or via a list provided to the keyword "pair".

        @param args: Listing of key, instrument pairs
        @type args: C{string}, L{Instrument}, etc.
        
        @param kwargs: A list of key word arguments that the constructor will
        accept
        
        @keyword pairs: Listing of key, instrument pairs
        @type pairs: C{list} of C{string}, L{Instrument} pairs
        """
        self.__inst_hash = {}

        pairlist = []
        if len(args) > 0:
            if len(args) % 2 != 0:
                raise RuntimeError("The list of arguments must be pairwise "\
                                   +"and proceed as: key1, inst1, key2, "\
                                   +"inst2 ...")
            # Everything is OK, go on
            else:
                pass

            pairlist.extend(args)

        else:
            try:
                pairlist = kwargs["pairs"]
            # If key is not present, don't do anything
            except KeyError:
                pass

        if len(pairlist) != 0:
            for i in range(0, len(pairlist), 2):
                self.__inst_hash[pairlist[i]] = pairlist[i+1]
        # No arguments or keywords given, do nothing
        else:
            pass

    def set_instrument(self, key, obj):
        """
        This function sets the instrument object to the given key name in the
        internal hash.

        @param key: The given key name for the instrument
        @type key: C{string}
        
        @param obj: The given instrument object
        @type obj: L{Instrument}
        """
        self.__inst_hash[key] = obj

    def get_instrument(self, key, **kwargs):
        """
        This function returns the instrument assigned to the given key in the
        internal hash.

        @param key: The given key name for the instrument
        @type key: C{string}
        
        @param kwargs: A list of keyword arguments that the function will
        accept

        
        @returns: The instrument object associated with the given key
        @rtype: L{Instrument}
        """
        return self.__inst_hash[key]

    def get_name(self):
        """
        This function obtains the instrument short name from the first
        instrument stored in the hash.

        @returns: The instrument short name
        @rtype: C{string}
        """
        tag = self.__inst_hash.keys()[0]
        return self.__inst_hash[tag].get_name()

    def get_primary(self, id=None, **kwargs):
        """
        This function obtains the primary flight path from the instrument
        object. If no ID is passed to the function, it returns the primary
        flight path from the first instrument in the hash table.

        @param id: The object containing the pixel ID
        @type id: L{SOM.SO}
        
        @param kwargs: A list of key word arguments that the function will
                       accept        


        @returns: The primary flight path and its associated error^2 for the
        requested instrument
        @rtype: C{tuple}
        """
        if id is None:
            tag = self.__inst_hash.keys()[0]
        else:
            tag = id[0]

        return self.__inst_hash[tag].get_primary(id, **kwargs)

    def get_secondary(self, id, **kwargs):
        """
        This function obtains the secondary flight path from the instrument
        object.

        @param id: The object containing the pixel ID
        @type id: L{SOM.SO}
        
        @param kwargs: A list of key word arguments that the function will
                       accept        


        @returns: The secondary flight path and its associated error^2 for the
        requested instrument
        @rtype: C{tuple}
        """
        return self.__inst_hash[id[0]].get_secondary(id, **kwargs)

    def get_total_path(self, id, **kwargs):
        """
        This function obtains the total flight path from the instrument
        object.

        @param id: The object containing the pixel ID
        @type id: L{SOM.SO}
        
        @param kwargs: A list of key word arguments that the function will
                       accept        


        @returns: The total flight path and its associated error^2 for the
        requested instrument
        @rtype: C{tuple}
        """
        return self.__inst_hash[id[0]].get_total_path(id, **kwargs)

    def get_polar(self, id, **kwargs):
        """
        This function obtains the polar angle from the instrument object.

        @param id: The object containing the pixel ID
        @type id: L{SOM.SO}
        
        @param kwargs: A list of key word arguments that the function will
                       accept        


        @returns: The polar angle and its associated error^2 for the requested
                  instrument
        @rtype: C{tuple}
        """
        return self.__inst_hash[id[0]].get_polar(id, **kwargs)

    def get_azimuthal(self, id, **kwargs):
        """
        This function obtains the azimuthal angle from the instrument object.

        @param id: The object containing the pixel ID
        @type id: L{SOM.SO}
        
        @param kwargs: A list of key word arguments that the function will
                       accept        


        @returns: The azimuthal angle and its associated error^2 for the
                  requested instrument
        @rtype: C{tuple}
        """
        return self.__inst_hash[id[0]].get_azimuthal(id, **kwargs)

    def get_x_pix_offset(self, id, **kwargs):
        """
        This function obtains the x pixel offset from the instrument object.

        @param id: The object containing the pixel ID
        @type id: L{SOM.SO}
        
        @param kwargs: A list of key word arguments that the function will
                       accept        


        @returns: The x pixel offset for the requested instrument
        @rtype: C{float}
        """
        return self.__inst_hash[id[0]].get_x_pix_offset(id, **kwargs)

    def get_y_pix_offset(self, id, **kwargs):
        """
        This function obtains the y pixel offset from the instrument object.

        @param id: The object containing the pixel ID
        @type id: L{SOM.SO}
        
        @param kwargs: A list of key word arguments that the function will
                       accept        


        @returns: The y pixel offset for the requested instrument
        @rtype: C{float}
        """
        return self.__inst_hash[id[0]].get_y_pix_offset(id, **kwargs)    

    def get_diff_geom(self, key, id, **kwargs):
        """
        This method obtains the specified differential geometry parameter from
        the instrument object

        @param key: The name of the differential geometry parameter to retrieve
        @type key: C{string}

        @param id: The object containing the pixel ID
        @type id: L{SOM.SO}

        @param kwargs: A list of keyword arguments that this function accepts
        and that internal functions will use.


        @returns: The differential geometry parameter value for the given
                  detector pixel
        @rtype: C{tuple}
        """
        return self.__inst_hash[id[0]].get_diff_geom(key, id, **kwargs)

    def get_diff_geom_keys(self):
        """
        This method retrieves the list of parameter names (keys) for the
        differential geometry information.

        @returns: The stored names of the differential geometry parameters
        @rtype: C{list}
        """
        tag = self.__inst_hash.keys()[0]
        return self.__inst_hash[tag].get_diff_geom_keys()
