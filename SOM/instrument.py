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
    """This is an abstract base class representing important
    geometrical information about the instrument.

    Parameters:
    -----------
    ->kwargs is a list of key word arguments that the function accepts:
         azimuthal = The values of the azimuthal angle
         azimuthal_err2 = The values of the square of the uncertainty in the
                     azimuthal angle
         azimuthal_selector = The name of the selector for the azimuthal angle
         instrument= The (abbreviated) name of the instrument
         polar = The values of the polar angle
         polar_err2 = The values of the square of the uncertainty in the
                     polar angle
         polar_selector = The name of the selector for the polar angle
         primary = The value of the primary flight path and the square of
                     its uncertainty
         secondary = The values of the secondary flight path
         secondary_err2 = The values of the square of the uncertainty in the 
                     secondary flight path
         secondary_selector = The name of the selector for the secondary
                              flight path
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
                self.__secondary_err2__=None
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
                self.__polar_err2__=None
        except KeyError:
            self.__polar_err2__=None

        # azimuthal angle
        try:
            self.__azimuthal__=kwargs["azimuthal"]
        except KeyError:
            self.__azimuthal__=None;
        try:
            self.__azimuthal_err2__=kwargs["azimuthal_err2"]
            if self.__azimuthal__==None:
                self.__azimuthal_err2__=None
        except KeyError:
            self.__azimuthal_err2__=None

        # the instrument name decides what selectors to chose
        try:
            inst=kwargs["instrument"]
            try:
                inst=inst.upper() #keys on uppercase version of instrument name
            except AttributeError:
                pass # errors will be picked up below
        except KeyError:
            inst=None

        try:
            extra=kwargs["extra"]
        except KeyError:
            extra=None

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
        elif inst == "REF_L":
            self.__azimuthal_selector__ = getIndexSelector("ISelector")
            self.__secondary_selector__ = getIndexSelector("IJSelector",
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
        import utils
        try:
            if utils.compare(self.__L0, other.get_primary()) != 0: 
                return False

        except:
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)
    
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
            offset=self.__polar_selector__.getIndex(id)
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
            offset=self.__azimuthal_selector__.getIndex(id)
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
