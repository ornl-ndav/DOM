class Instrument:
    """This is an abstract base class representing important
    geometrical information about the instrument."""
    def __init__(self):
        pass
    
    def get_primary(id=None):
        """The primary flight path (neutronic distance from moderator
        to sample)"""
        return 0

    def get_secondary(id=None):
        """The secondary flight path (neutronic distance from sample
        to detector)"""
        return 0

    def get_polar(id=None):
        """The polar angle (angle between incident beam and detector)"""
        return 0

    def get_azimuthal(id=None):
        """The azimuthal angle (angle between plane and detector)"""
        return 0
