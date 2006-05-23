class Instrument:
    """This is an abstract base class representing important
    geometrical information about the instrument.

    Parameters:
    -----------
    ->kwargs is a list of key word arguments that the function accepts:
         azimuthal = The values of the azimuthal angle
         azimuthal_err2 = The values of the square of the uncertainty in the
                     azimuthal angle
         instrument= The (abbreviated) name of the instrument
         polar = The values of the polar angle
         polar_err2 = The values of the square of the uncertainty in the
                     polar angle
         primary = The value of the primary flight path and the square of
                     its uncertainty
         secondary = The values of the secondary flight path
         secondary_err2 = The values of the square of the uncertainty in the 
                     secondary flight path
    """
    def __init__(self,**kwargs):
        # primary flight path
        try:
            self.__L0=kwargs["primary"]
        except KeyError:
            self.__L0=None
            
        #secondary flight path
        try:
            self.__secondary__=kwargs["secondary"]
        except KeyError:
            self.__secondary__=None
        try:
            self.__secondary_err2__=kwargs["secondary_err2"]
            if self.__secondary__==None:
                raise AssertionError,"Cannot set uncertainty in secondary "\
                      +"flight path without value"
        except KeyError:
            self.__secondary_err2__=None

        # polar angle
        try:
            self.__polar__=kwargs["polar"]
        except KeyError:
            self.__polar__=None;
        try:
            self.__polar_err2__=kwargs["polar_err2"]
            if self.__polar__==None:
                raise AssertionError,"Cannot set uncertainty in polar angle "\
                      +"without value"
        except KeyError:
            self.__polar_err2__=None

        # azimuthal angle
        try:
            self.__azimuthal__=kwargs["azimuthal"]
        except KeyError:
            self.__azimuthal__=None;
        try:
            self.__azimutahl_err2__=kwargs["azimuthal_err2"]
            if self.__azimutahl__==None:
                raise AssertionError,"Cannot set uncertainty in azimuthal "\
                      +"angle without value"
        except KeyError:
            self.__azimuthal_err2__=None

        # the instrument name decides what selectors to chose
        try:
            inst=kwargs["instrument"]
            inst=inst.upper() # keys on uppercase version of instrument name
        except KeyError:
            raise AssertionError,"Must specify instrument name"

        # use the instrument name to set the selectors
        from indexselector import getIndexSelector
        if inst=="BSS":
            self.__azimuthal_selector__ = None;
            self.__polar_selector__     = getIndexSelector("ISelector")
            self.__secondary_selector__ = getIndexSelector("JSelector")
        else:
            raise RuntimeError,"Do not understand instrument: \""+inst+"\""
    
    def get_primary(self,id=None,**kwargs):
        """The primary flight path (neutronic distance from moderator
        to sample) in meters.

        Keyword arguments:
         units="meter" to specify what units the returned value will be in."""

        # parse the keywords
        units=__get_units__(kwargs,"meter")

        # return the result
        if self.__L0==None:
            raise RuntimeError,"Primary flight path is not defined"
        if(units=="meter"):
            return self.__L0
        else:
            raise RuntimeError,"Do not know how to convert to \"%s\"" % units

    def set_primary(self,distance,**kwargs):
        """The primary flight path (neutronic distance from moderator
        to sample) in meters."""
        # fix the units
        units=__get_units__(kwargs,"meter")
        if units!="meter":
            raise RuntimeError,"Do not understand units \"%s\"" % units

        # fix the value
        distance=__standardize_value__(distance)

        # set the value
        self.__L0=distance

    def get_secondary(self,id=None,**kwargs):
        """The secondary flight path (neutronic distance from sample
        to detector) in meters

        Keyword arguments:
         units="meter" to specify what units the returned value will be in."""
        try:
            offset=self.__secondary_selector__.getIndex(id)
        except AttributeError:
            raise RuntimeError,"Do not have information for selecting " \
                  +"correct secondary flight path"

        try:
            val=self.__secondary__[offset]
        except TypeError:
            raise RuntimeError,"Do not have information for secondary " \
                  +"flight path"
        
        try:
            err2=self.__secondary_err2__[offset]
            return (val,err2)
        except TypeError:
            return (val,0.)

    def get_total_path(self,id=None,**kwargs):
        """The total flight path (neutronic distance from sample
        to detector) in meters

        Keyword arguments:
         units="meter" to specify what units the returned value will be in."""
        L1=self.get_primary(**kwargs)
        L2=self.get_secondary(id,**kwargs)

        return (L1[0]+L2[0],L1[1]+L2[1])

    def get_polar(self,id=None,**kwargs):
        """The polar angle (angle between incident beam and detector)
        in degrees

        Keyword arguments:
         units="radian" to specify what units the returned value will be in."""
        try:
            offset=self.__polar_selctor__.getIndex(id)
        except AttributeError:
            raise RuntimeError,"Do not have information for selecting " \
                  +"correct polar angle"

        try:
            val=self.__polar__[offset]
        except TypeError:
            raise RuntimeError,"Do not have information for polar angle"
        
        try:
            err2=self.__polar_err2__[offset]
            return (val,err2)
        except TypeError:
            return (val,0.)

    def get_azimuthal(self,id=None,**kwargs):
        """The azimuthal angle (angle between plane and detector) in
        degrees

        Keyword arguments:
         units="radian" to specify what units the returned value will be in."""
        try:
            offset=self.__azimuthal_selctor__.getIndex(id)
        except AttributeError:
            raise RuntimeError,"Do not have information for selecting " \
                  +"correct azimuthal angle"

        try:
            val=self.__azimuthal__[offset]
        except TypeError:
            raise RuntimeError,"Do not have information for azumuthal angle"
        
        try:
            err2=self.__azimuthal_err2__[offset]
            return (val,err2)
        except TypeError:
            return (val,0.)

def __standardize_units__(units,default_units):
    # return early if the requested and specified are the same
    if units==default_units:
        return default_units

    # check if it is just plural form of the default units
    if units==default_units+"s":
        return default_units

    # the real work of standardization
    if units=="m" or units=="meter" or units=="meters" \
           or units=="metre" or units=="metres":
        return "meter"
    if units=="degree" or units=="degrees":
        return "degree"
    if units=="radian" or units=="radians":
        return "radian"

    # give up
    raise RuntimeError,"Do not understand units \"%s\"" % units

def __get_units__(kwargs,default_units):
    # get the value out of the hashmap
    if not kwargs.has_key("units"):
        return default_units
    units=kwargs["units"]

    # let somebody else do the work
    return __standardize_units__(units,default_units)

def __standardize_value__(thing):
    try:
        if len(thing)!=2:
            raise RuntimeError,"Cannot set value \"%s\"",str(thing)
        value=float(thing[0])
        err2=float(thing[1])
        return (value,err2)
    except TypeError:
        return (float(thing),0.)
