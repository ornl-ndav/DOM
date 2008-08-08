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

class Instrument:
    """
    This is an abstract base class representing important geometrical
    information about the instrument.

    @ivar __inst__: The instrument short name
    @type __inst__: C{string}

    @ivar __L0: The instrument's primary (moderator to sample) flight path.
    @type __L0: C{tuple}

    @ivar __L1: The instrument's main secondary (sample to detector) flight
                path.
    @type __L1: C{tuple}

    @ivar __azimuthal__: The instrument's detector pixel azimuthal angles
    @type __azimuthal__: C{list} of C{tuple}s or C{tuple}

    @ivar __azimuthal_err2__: The instrument's detector pixel squared
                              uncertainties in the azimuthal angles
    @type __azimuthal_err2__: C{list} of C{tuple}s or C{tuple}

    @ivar __azimuthal_selector__: The appropriate index selection for
                                  retrieving the instrument's detector pixel
                                  azimuthal angles.
    @type __azimuthal_selector__: L{IndexSelectorBase}

    @ivar __polar__: The instrument's detector pixel polar angles
    @type __polar__: C{list} of C{tuple}s or C{tuple}

    @ivar __polar_err2__: The instrument's detector pixel squared
                              uncertainties in the polar angles
    @type __polar_err2__: C{list} of C{tuple}s or C{tuple}

    @ivar __polar_selector__: The appropriate index selection for retrieving
                              the instrument's detector pixel polar angles.
    @type __polar_selector__: L{IndexSelectorBase}

    @ivar __secondary__: The instrument's detector pixel secondary (sample to
                         detector) flight paths
    @type __secondary__: C{list} of C{tuple}s or C{tuple}

    @ivar __secondary_err2__: The instrument's detector pixel squared
                              uncertainties in the secondary flight paths
    @type __secondary_err2__: C{list} of C{tuple}s or C{tuple}

    @ivar __secondary_selector__: The appropriate index selection for
                                  retrieving the instrument's detector pixel
                                  secondary flight paths.
    @type __secondary_selector__: L{IndexSelectorBase}

    @ivar __x_pix_offset__: The instrument's x detector pixel offset
    @type __x_pix_offset__: C{list} of C{tuple}s or C{tuple}

    @ivar __xoff_selector__: The appropriate index selection for retrieving
                             the instrument's x detector pixel offset
    @type __xoff_selector__: L{IndexSelectorBase}
    
    @ivar __y_pix_offset__: The instrument's y detector pixel offset
    @type __y_pix_offset__: C{list} of C{tuple}s or C{tuple}    

    @ivar __yoff_selector__: The appropriate index selection for retrieving
                             the instrument's y detector pixel offset
    @type __yoff_selector__: L{IndexSelectorBase}

    @ivar __diff_geom__: A dictionary holding the differential geometry
                         information for the instrument. Each dictionary entry
                         will have a key name based on the particular
                         parameter. The value for the associated key will be
                         a C{tuple} of the following: a C{nessi_list.NessiList}
                         of values, a C{nessi_list.NessiList} of error^2s,
                         units of the parameter (C{string}) and a concrete
                         instance of a C{IndexSelectorBase}.
    @type __diff_geom__: C{dict}

    @ivar __diff_geom_keys__: A cache of the keys for the differential geometry
                              information.
    @type __diff_geom_keys__: C{list}
    """

    def __init__(self, **kwargs):
        """
        Class constructor
        
        @param kwargs: A list of key word arguments that the class accepts:

        @keyword instrument: The short name of the instrument.
        @type instrument: C{string}
         
        @keyword azimuthal: The values of the azimuthal angle.
        @type azimuthal: C{list} of C{tuple}s or C{tuple}
    
        @keyword azimuthal_err2: The values of the square of the uncertainty
                                 in the azimuthal angle.
        @type azimuthal_err2: C{list} of C{tuple}s or C{tuple}
    
        @keyword azimuthal_selector: The name of the index selector for the
                                     azimuthal angle.
        @type azimuthal_selector: C{string}

        @keyword det_secondary: The values of the detector bank secondary
        flight path and it's associated uncertainty.
        @type det_secondary: C{tuple}
        
        @keyword polar: The values of the polar angle.
        @type polar: C{list} of C{tuple}s or C{tuple}
        
        @keyword polar_err2: The values of the square of the uncertainty in the
                             polar angle.
        @type polar_err2: C{list} of C{tuple}s or C{tuple}
        
        @keyword polar_selector: The name of the index selector for the polar
                                 angle.
        @type polar_selector: C{string}
        
        @keyword secondary: The values of the secondary flight path.
        @type secondary: C{list} of C{tuple}s or C{tuple}
        
        @keyword secondary_err2: The values of the square of the uncertainty
                                 in the secondary flight path.
        @type secondary_err2: C{list} of C{tuple}s or C{tuple}
        
        @keyword secondary_selector: The name of the index selector for the
                                     secondary flight path.
        @type secondary_selector: C{string}
        
        @keyword extra: The maximum value for the fastest running index. This
                        is necessary if the L{IJSelector} is used.
        @type extra: C{int}

        @keyword diff_geom: A dictionary containing the differential geometry
                            for the instrument.
        @type diff_geom: C{dict}

        @keyword x_pix_offset: The values of the x pixel offsets.
        @type x_pix_offset: C{list} of C{tuple}s or C{tuple}

        @keyword y_pix_offset: The values of the y pixel offsets.
        @type y_pix_offset: C{list} of C{tuple}s or C{tuple}
        """
        # primary flight path
        try:
            self.__L0 = kwargs["primary"]
        except KeyError:
            self.__L0 = None

        # detector secondary flight path
        try:
            self.__L1 = kwargs["det_secondary"]
        except KeyError:
            self.__L1 = None            
        
        #secondary flight path
        try:
            self.__secondary__ = kwargs["secondary"]
        except KeyError:
            self.__secondary__ = None
        try:
            self.__secondary_err2__ = kwargs["secondary_err2"]
            if self.__secondary__ is None:
                self.__secondary_err2__ = None
        except KeyError:
            self.__secondary_err2__ = None

        # polar angle
        try:
            self.__polar__ = kwargs["polar"]
        except KeyError:
            self.__polar__ = None;
        try:
            self.__polar_err2__ = kwargs["polar_err2"]
            if self.__polar__ is None:
                self.__polar_err2__ = None
        except KeyError:
            self.__polar_err2__ = None

        # azimuthal angle
        try:
            self.__azimuthal__ = kwargs["azimuthal"]
        except KeyError:
            self.__azimuthal__ = None;
        try:
            self.__azimuthal_err2__ = kwargs["azimuthal_err2"]
            if self.__azimuthal__ is None:
                self.__azimuthal_err2__ = None
        except KeyError:
            self.__azimuthal_err2__ = None

        # set the instrument short name
        try:
            self.__inst__ = kwargs["instrument"]
            try:
                # uppercase version of instrument name
                self.__inst__ = self.__inst__.upper()

            except AttributeError:
                self.__inst__ = ""
        except KeyError:
            self.__inst__ = ""

        try:
            extra = kwargs["extra"]
        except KeyError:
            extra = None

        # Set the instrument differential geometry dictionary (if present)
        try:
            self.__diff_geom__ = kwargs["diff_geom"]
            if self.__diff_geom__ is not None:
                self.__diff_geom_keys__ = self.__diff_geom__.keys()
            else:
                self.__diff_geom_keys__ = None                
        except KeyError:
            self.__diff_geom__ = None
            self.__diff_geom_keys__ = None

        # x pixel offsets
        try:
            self.__x_pix_offset__ = kwargs["x_pix_offset"]
        except KeyError:
            self.__x_pix_offset__ = None;

        # y pixel offsets
        try:
            self.__y_pix_offset__ = kwargs["y_pix_offset"]
        except KeyError:
            self.__y_pix_offset__ = None;
            
        # set the selectors
        from indexselector import getIndexSelector

        self.__azimuthal_selector__ = getIndexSelector("IJSelector", Nj=extra)
        self.__polar_selector__     = getIndexSelector("IJSelector", Nj=extra)
        self.__secondary_selector__ = getIndexSelector("IJSelector", Nj=extra)
        self.__xoff_selector__      = getIndexSelector("ISelector")
        self.__yoff_selector__      = getIndexSelector("JSelector")

        # override capability mainly for backwards compatibility
        try:
            az_sel_name = kwargs["azimuthal_selector"]
            if az_sel_name is not None:
                self.__azimuthal_selector__ = getIndexSelector(az_sel_name,
                                                               Nj=extra)
        except KeyError:
            pass

        try:
            pol_sel_name = kwargs["polar_selector"]
            if pol_sel_name is not None:
                self.__polar_selector__ = getIndexSelector(pol_sel_name,
                                                           Nj=extra)
        except KeyError:
            pass

        try:
            sec_sel_name = kwargs["secondary_selector"]
            if sec_sel_name is not None:
                self.__secondary_selector__ = getIndexSelector(sec_sel_name,
                                                               Nj=extra)
        except KeyError:
            pass        

    def __eq__(self, other):
        """
        This method checks to see if the incoming C{Instrument} object and the
        current one are equal.

        @param other: Object to check for equality
        @type other: C{Instrument}


        @return: I{True} if the C{Instrument} objects are equal, I{False} if
                 they are not
        @rtype: C{boolean}
        """        
        import utils
        try:
            if utils.compare(self.__L0, other.get_primary()) != 0: 
                return False
        except:
            return False

        return True

    def __ne__(self, other):
        """
        This method checks to see if the incoming C{Instrument} object and the
        current one are not equal.

        @param other: Object to check for equality
        @type other: C{Instrument}


        @return: I{True} if the C{Instrument} objects are not equal, I{False}
                 if they are
        @rtype: C{boolean}
        """        
        return not self.__eq__(other)

    def get_name(self):
        """
        This function obtains the instrument short name.

        @returns: The instrument short name
        @rtype: C{string}
        """
        return self.__inst__
    
    def get_primary(self, id=None, **kwargs):
        """
        This method returns the primary flight path in meters.

        @param id: The object containing the pixel ID
        @type id: L{SOM.SO}

        @param kwargs: A list of keyword arguments that this function accepts
        and that internal functions will use.


        @returns: The instrument's primary flight path
        @rtype: C{tuple}
        """
        # parse the keywords
        units=__get_units__(kwargs, "meter")

        # return the result
        if self.__L0 is None:
            raise RuntimeError("Primary flight path is not defined")
        
        if units == "meter":
            return self.__L0
        else:
            raise RuntimeError("Do not know how to convert to \"%s\"" % units)

    def set_primary(self, distance, **kwargs):
        """
        This method sets the primary flight path for the instrument.

        @param distance: The primary flight path and its associated error^2
        @type distance: C{tuple}

        @param kwargs: A list of keyword arguments that this function accepts
        and that internal functions will use.        
        """
        # fix the units
        units = __get_units__(kwargs, "meter")
        
        if units != "meter":
            raise RuntimeError("Do not understand units \"%s\"" % units)

        # fix the value
        distance = __standardize_value__(distance)

        # set the value
        self.__L0 = distance

    def get_det_secondary(self, id=None, **kwargs):
        """
        This method returns the detector bank secondary flight path in meters.

        @param id: The object containing the pixel ID
        @type id: L{SOM.SO}

        @param kwargs: A list of keyword arguments that this function accepts
        and that internal functions will use.


        @returns: The instrument's detector bank secondary flight path
        @rtype: C{tuple}
        """
        # parse the keywords
        units=__get_units__(kwargs, "meter")

        # return the result
        if self.__L1 is None:
            raise RuntimeError("Detector secondary flight path is not defined")
        
        if units == "meter":
            return self.__L1
        else:
            raise RuntimeError("Do not know how to convert to \"%s\"" % units)

    def get_secondary(self, id=None, **kwargs):
        """
        This method returns the secondary flight path for a detector pixel in
        the instrument. 

        @param id: The object containing the pixel ID
        @type id: L{SOM.SO}

        @param kwargs: A list of keyword arguments that this function accepts
        and that internal functions will use.


        @returns: The detector pixel secondary flight path
        @rtype: C{tuple}
        """
        try:
            offset = self.__secondary_selector__.getIndex(id)
        except AttributeError:
            raise RuntimeError("Do not have information for selecting " \
                               +"correct secondary flight path")

        try:
            val = self.__secondary__[offset]
        except TypeError:
            raise RuntimeError("Do not have information for secondary " \
                               +"flight path")
        
        try:
            err2 = self.__secondary_err2__[offset]
            return (val, err2)
        except TypeError:
            return (val, 0.)

    def get_total_path(self, id=None, **kwargs):
        """
        This method returns the total flight path for a detector pixel in the
        instrument.

        @param id: The object containing the pixel ID
        @type id: L{SOM.SO}

        @param kwargs: A list of keyword arguments that this function accepts
        and that internal functions will use.

        @keyword det_secondary: A flag that signals the function to add the
                                detector secondary flight path for the total
                                flight path. The default is I{False}.
        @type det_secondary: C{bool}


        @returns: The detector pixel total flight path
        @rtype: C{tuple}
        """
        try:
            det_secondary = kwargs["det_secondary"]
        except KeyError:
            det_secondary = False
        
        L1 = self.get_primary(**kwargs)
        if not det_secondary:
            L2 = self.get_secondary(id, **kwargs)
        else:
            L2 = self.get_det_secondary(id, **kwargs)

        return (L1[0] + L2[0], L1[1] + L2[1])

    def get_polar(self, id=None, **kwargs):
        """
        This method returns the polar angle for a detector pixel in the
        instrument.

        @param id: The object containing the pixel ID
        @type id: L{SOM.SO}

        @param kwargs: A list of keyword arguments that this function accepts
        and that internal functions will use.


        @returns: The detector pixel polar angle
        @rtype: C{tuple}        
        """
        try:
            offset = self.__polar_selector__.getIndex(id)
        except AttributeError:
            raise RuntimeError("Do not have information for selecting " \
                               +"correct polar angle")

        try:
            val = self.__polar__[offset]
        except TypeError:
            raise RuntimeError("Do not have information for polar angle")
        
        try:
            err2 = self.__polar_err2__[offset]
            return (val, err2)
        except TypeError:
            return (val, 0.)

    def get_azimuthal(self, id=None, **kwargs):
        """
        This method returns the azimuthal angle for a detector pixel in the
        instrument.

        @param id: The object containing the pixel ID
        @type id: L{SOM.SO}
        
        @param kwargs: A list of keyword arguments that this function accepts
        and that internal functions will use.


        @returns: The detector pixel azimuthal angle
        @rtype: C{tuple}
        """
        try:
            offset = self.__azimuthal_selector__.getIndex(id)
        except AttributeError:
            raise RuntimeError("Do not have information for selecting " \
                               +"correct azimuthal angle")

        try:
            val = self.__azimuthal__[offset]
        except TypeError:
            raise RuntimeError("Do not have information for azumuthal angle")
        
        try:
            err2 = self.__azimuthal_err2__[offset]
            return (val, err2)
        except TypeError:
            return (val, 0.)

    def get_x_pix_offset(self, id=None, **kwargs):
        """
        This method returns the x pixel offset for a detector pixel in the
        instrument.

        @param id: The object containing the pixel ID
        @type id: L{SOM.SO}
        
        @param kwargs: A list of keyword arguments that this function accepts
        and that internal functions will use.


        @returns: The detector x pixel offset
        @rtype: C{float}
        """
        try:
            offset = self.__xoff_selector__.getIndex(id)
        except AttributeError:
            raise RuntimeError("Do not have information for selecting " \
                               +"correct x pixel offset")

        try:
            return self.__x_pix_offset__[offset]
        except TypeError:
            raise RuntimeError("Do not have information for x pixel offset")

    def get_y_pix_offset(self, id=None, **kwargs):
        """
        This method returns the y pixel offset for a detector pixel in the
        instrument.

        @param id: The object containing the pixel ID
        @type id: L{SOM.SO}
        
        @param kwargs: A list of keyword arguments that this function accepts
        and that internal functions will use.


        @returns: The detector y pixel offset
        @rtype: C{float}
        """
        try:
            offset = self.__yoff_selector__.getIndex(id)
        except AttributeError:
            raise RuntimeError("Do not have information for selecting " \
                               +"correct y pixel offset")

        try:
            return self.__y_pix_offset__[offset]
        except TypeError:
            raise RuntimeError("Do not have information for y pixel offset")
        
    def get_diff_geom(self, key, id=None, **kwargs):
        """
        This method retrieves the differential geometry value and error^2 for
        the given pixel ID.

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
        try:
            try:
                offset = self.__diff_geom__[key][-1].getIndex(id)
            except AttributeError:
                raise RuntimeError("Do not have information for selecting " \
                                   +"correct differential geometry parameter "\
                                   +"%s" % key)
            try:
                val = self.__diff_geom__[key][0][offset]
            except TypeError:
                raise RuntimeError("Do not have information for differential "\
                                   +"geometry parameter %s" % key)
            try:
                err2 = self.__diff_geom__[key][1][offset]
                return (val, err2)
            except TypeError:
                return (val, 0.)
        except KeyError:
            raise RuntimeError("Differential geometry key %s not found in "\
                               +"the following list: %s" % \
                               (key, " ".join(self.__diff_geom_keys__)))
        
    def get_diff_geom_keys(self):
        """
        This method retrieves the list of parameter names (keys) for the
        differential geometry information.
        
        @returns: The stored names of the differential geometry parameters
        @rtype: C{list}
        """
        return self.__diff_geom_keys__
                               
def __standardize_units__(units, default_units):
    """
    This is a private helper function which standardizes certain unit name
    variations to a single given name.

    @param units: The unit name to standardize
    @type units: C{string}

    @param default_units: The unit name to standardize to
    @type default_units: C{string}


    @returns: The standardized unit name
    @rtype: C{string}
    """
    # return early if the requested and specified are the same
    if units == default_units:
        return default_units

    # check if it is just plural form of the default units
    if units == default_units + "s":
        return default_units

    # the real work of standardization
    if units == "m" or units == "meter" or units == "meters" \
           or units == "metre" or units == "metres":
        return "meter"
    if units == "degree" or units == "degrees":
        return "degree"
    if units == "radian" or units == "radians":
        return "radian"

    # give up
    raise RuntimeError("Do not understand units \"%s\"" % units)

def __get_units__(kwargs, default_units):
    """
    This is a private helper function which scans a dictionary looking for
    the keyword I{units} and obtaining the value associated with that key.

    @param kwargs: A list of keyword arguments that this function scans
    @type kwargs: C{dict}


    @returns: The units for a given value
    @rtype: C{string}
    """
    # get the value out of the hashmap
    if not kwargs.has_key("units"):
        return default_units
    units = kwargs["units"]

    # let somebody else do the work
    return __standardize_units__(units, default_units)

def __standardize_value__(thing):
    """
    This is a private helper function that standardizes a tuple of information
    such that there is always a square uncertainty for every corresponding
    value.

    @param thing: A value and possible associated square uncertainty
    @type thing: C{tuple}, C{float} or C{int}


    @return: A standardized object containing the value and the square
    uncertainty.
    @rtype: C{tuple}
    """
    try:
        if len(thing) != 2:
            raise RuntimeError("Cannot set value \"%s\"", str(thing))
        value = float(thing[0])
        err2 = float(thing[1])
        return (value, err2)
    except TypeError:
        return (float(thing), 0.)
