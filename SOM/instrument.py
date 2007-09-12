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

    @ivar __L0: The instrument's primary (moderator to sample) flight path.
    @type __L0: C{tuple}

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
        """
        # primary flight path
        try:
            self.__L0 = kwargs["primary"]
        except KeyError:
            self.__L0 = None
            
        #secondary flight path
        try:
            self.__secondary__ = kwargs["secondary"]
        except KeyError:
            self.__secondary__ = None
        try:
            self.__secondary_err2__ = kwargs["secondary_err2"]
            if self.__secondary__==None:
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
            if self.__polar__==None:
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
            if self.__azimuthal__==None:
                self.__azimuthal_err2__ = None
        except KeyError:
            self.__azimuthal_err2__ = None

        # the instrument name decides what selectors to chose
        try:
            inst = kwargs["instrument"]
            try:
                #keys on uppercase version of instrument name
                inst =inst.upper()

            except AttributeError:
                pass # errors will be picked up below
        except KeyError:
            inst = None

        try:
            extra = kwargs["extra"]
        except KeyError:
            extra = None

        # use the instrument name to set the selectors
        from indexselector import getIndexSelector
        if inst==None:
            self.__azimuthal_selector__ = None
            self.__polar_selector__     = None
            self.__secondary_selector__ = None
        elif inst=="BSS":
            self.__azimuthal_selector__ = None
            self.__polar_selector__     = getIndexSelector("IJSelector",
                                                           Nj=extra)
            self.__secondary_selector__ = getIndexSelector("JSelector")
        elif inst=="BSS_DIFF":
            self.__azimuthal_selector__ = getIndexSelector("IJSelector",
                                                           Nj=extra)
            self.__polar_selector__     = getIndexSelector("IJSelector",
                                                           Nj=extra)
            self.__secondary_selector__ = getIndexSelector("IJSelector",
                                                           Nj=extra)
        elif inst == "REF_M":
            self.__azimuthal_selector__ = getIndexSelector("JSelector")
            self.__secondary_selector__ = getIndexSelector("IJSelector",
                                                           Nj=extra)
            self.__polar_selector__     = getIndexSelector("IJSelector",
                                                           Nj=extra)        
        elif inst == "REF_L":
            self.__azimuthal_selector__ = getIndexSelector("ISelector")
            self.__secondary_selector__ = getIndexSelector("IJSelector",
                                                           Nj=extra)
            self.__polar_selector__     = getIndexSelector("IJSelector",
                                                           Nj=extra)         
        elif inst == "GLAD":
            self.__azimuthal_selector__ = getIndexSelector("JSelector")
            self.__polar_selector__     = getIndexSelector("IJSelector",
                                                           Nj=extra)
            self.__secondary_selector__ = getIndexSelector("IJSelector",
                                                           Nj=extra)
            
        else:
            raise RuntimeError,"Do not understand instrument: \""+inst+"\""

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
        if self.__L0==None:
            raise RuntimeError,"Primary flight path is not defined"
        if(units=="meter"):
            return self.__L0
        else:
            raise RuntimeError,"Do not know how to convert to \"%s\"" % units

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
        if units!="meter":
            raise RuntimeError,"Do not understand units \"%s\"" % units

        # fix the value
        distance = __standardize_value__(distance)

        # set the value
        self.__L0 = distance

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
            raise RuntimeError,"Do not have information for selecting " \
                  +"correct secondary flight path"

        try:
            val = self.__secondary__[offset]
        except TypeError:
            raise RuntimeError,"Do not have information for secondary " \
                  +"flight path"
        
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


        @returns: The detector pixel total flight path
        @rtype: C{tuple}
        """
        L1 = self.get_primary(**kwargs)
        L2 = self.get_secondary(id, **kwargs)

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
            raise RuntimeError,"Do not have information for selecting " \
                  +"correct polar angle"

        try:
            val = self.__polar__[offset]
        except TypeError:
            raise RuntimeError,"Do not have information for polar angle"
        
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
            raise RuntimeError,"Do not have information for selecting " \
                  +"correct azimuthal angle"

        try:
            val = self.__azimuthal__[offset]
        except TypeError:
            raise RuntimeError,"Do not have information for azumuthal angle"
        
        try:
            err2 = self.__azimuthal_err2__[offset]
            return (val, err2)
        except TypeError:
            return (val, 0.)

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
        if len(thing)!=2:
            raise RuntimeError,"Cannot set value \"%s\"",str(thing)
        value = float(thing[0])
        err2 = float(thing[1])
        return (value, err2)
    except TypeError:
        return (float(thing), 0.)
