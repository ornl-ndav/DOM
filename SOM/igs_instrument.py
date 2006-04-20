from instrument import Instrument
class IGS_Instrument(Instrument):
    def __init__(self):
        Instrument.__init__(self)
        self.set_primary(84)
        self.__L2=None
    
    def get_L2(self,id=None,**kwargs):
        units=__get_units__(kwargs,"meter")
        if units=="meter":
            return self.__L2
        else:
            raise RuntimeError,"Do not understand units \"%s\"" % units
    
    def set_L2(self,distance,units="meter",id=None):
        units=__standardize_units__(units,"meter")
        self.__L2=distance

    def get_L3(self,id=None,**kwargs):
        units=__get_units__(kwargs,"meter")
        if units=="meter":
            return 0.
        else:
            raise RuntimeError,"Do not understand units \"%s\"" % units

    def set_L3(self,distances,units="meter",id=None):
        units=__standardize_units__(units,"meter")

    def get_secondary(self,id=None,**kwargs):
        """The secondary flight path (neutronic distance from sample
        to detector) in meters

        Keyword arguments:
         units="meter" to specify what units the returned value will be in."""

        # parse the keywords
        units=__get_units__(kwargs,"meter")

        # calculate the position
        result=self.get_L2(id)+self.get_L3(id)

        if units=="meter":
            return result
        else:
            raise RuntimeError,"Do not understand units \"%s\"" % units

    def get_polar(self,id=None,**kwargs):
        """The polar angle (angle between incident beam and detector)
        in degrees

        Keyword arguments:
         units="radian" to specify what units the returned value will be in."""

        # parse the keywords
        units=__get_units__(kwargs,"degree")

        #import math
        #math.degrees
        #math.radians <- degrees to radians
        raise RuntimeError,"Polar angle is not defined"

    def set_polar(self,angles,units="radian",id=None):
        units=__standardize_units__(units,"radian")

    def get_azimuthal(self,id=None,**kwargs):
        """The azimuthal angle (angle between plane and detector) in
        degrees

        Keyword arguments:
         units="radian" to specify what units the returned value will be in."""

        # parse the keywords
        units=__get_units__(kwargs,"degree")

        raise RuntimeError,"Azimuthal angle is not defined"

    def set_azimuthal(self,angles,units="radian",id=None):
        units=__standardize_units__(units,"radian")

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
            return default_val
        units=kwargs["units"]

        # let somebody else do the work
        return __standardize_units__(units,default_units)

