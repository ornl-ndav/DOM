class Instrument:
    """This is an abstract base class representing important
    geometrical information about the instrument."""
    def __init__(self):
        self.__L0=None
    
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

    def get_secondary(self,id=None,**kwags):
        """The secondary flight path (neutronic distance from sample
        to detector) in meters

        Keyword arguments:
         units="meter" to specify what units the returned value will be in."""
        raise RuntimeError,"Secondary flight path is not defined"

    def get_polar(self,id=None,**kwargs):
        """The polar angle (angle between incident beam and detector)
        in degrees

        Keyword arguments:
         units="radian" to specify what units the returned value will be in."""
        raise RuntimeError,"Polar angle is not defined"

    def get_azimuthal(self,id=None,**kwargs):
        """The azimuthal angle (angle between plane and detector) in
        degrees

        Keyword arguments:
         units="radian" to specify what units the returned value will be in."""
        raise RuntimeError,"Azimuthal angle is not defined"

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
