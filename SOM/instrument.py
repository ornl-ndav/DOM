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
        if self.__L0==None:
            raise RuntimeError,"Primary flight path is not defined"
        return self.__L0

    def set_primary(self,distance,units="meter"):
        if units=="m" or units=="meter" or units=="meters" \
               or units=="metre" or units=="metres":
            self.__L0=float(distance)
        else:
            raise RuntimeError,"Do not understand units \"%s\"" % units

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
