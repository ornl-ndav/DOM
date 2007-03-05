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

from instrument import Instrument
from instrument import __get_units__
from instrument import __standardize_value__

class IGS_Instrument(Instrument):
    def __init__(self):
        Instrument.__init__(self)
        self.set_primary(84)
        self.set_L2(2.499)
    
    def get_L2(self,id=None,**kwargs):
        units=__get_units__(kwargs,"meter")
        if units=="meter":
            return self.__L2
        else:
            raise RuntimeError,"Do not understand units \"%s\"" % units
    
    def set_L2(self,distance,id=None,**kwargs):
        # fix the units
        units=__get_units__(kwargs,"meter")
        if units!="meter":
            raise RuntimeError,"Do not understand units \"%s\"" % units

        # fix the value
        distance=__standardize_value__(distance)

        # set the value
        self.__L2=distance

    def get_L3(self,id=None,**kwargs):
        units=__get_units__(kwargs,"meter")
        if units!="meter":
            raise RuntimeError,"Do not understand units \"%s\"" % units

        return (0.,0.)

    def set_L3(self,distances,id=None,**kwargs):
        # fix the units
        units=__get_units__(kwargs,"meter")
        if units!="meter":
            raise RuntimeError,"Do not understand units \"%s\"" % units

    def get_secondary(self,id=None,**kwargs):
        """The secondary flight path (neutronic distance from sample
        to detector) in meters

        Keyword arguments:
         units="meter" to specify what units the returned value will be in."""

        # fix the units
        units=__get_units__(kwargs,"meter")
        if units!="meter":
            raise RuntimeError,"Do not understand units \"%s\"" % units

        # calculate the position
        L2=self.get_L2(id)
        L3=self.get_L3(id)
        value=L2[0]+L3[0]
        err2=L2[1]+L3[1]

        # return the result
        return (value,err2)

    def get_polar(self,id=None,**kwargs):
        """The polar angle (angle between incident beam and detector)
        in degrees

        Keyword arguments:
         units="radian" to specify what units the returned value will be in."""

        # fix the units
        units=__get_units__(kwargs,"radian")
        if units!="radian":
            raise RuntimeError,"Do not understand units \"%s\"" % units

        #import math
        #math.degrees
        #math.radians <- degrees to radians
        return (0.,0.)

    def set_polar(self,angles,id=None,**kwargs):
        units=__get_units__(kwargs,"radian")

    def get_azimuthal(self,id=None,**kwargs):
        """The azimuthal angle (angle between plane and detector) in
        degrees

        Keyword arguments:
         units="radian" to specify what units the returned value will be in."""

        # fix the units
        units=__get_units__(kwargs,"radian")
        if units!="radian":
            raise RuntimeError,"Do not understand units \"%s\"" % units

        return (0.,0.)

    def set_azimuthal(self,angles,id=None,**kwargs):
        units=__get_units__(kwargs,"radian")
