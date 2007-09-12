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

class AttributeList(dict):
    """
    This class is the container for the scientific metadata. The class is
    dervied from C{dict} which gives it a hash table capability that will
    provide extensibility for the metadata. The instrument geometry and sample
    information are held separately and can be accessed without the use of
    dictionary keys.

    @ivar instrument: This variable contains the instrument geometry
                      information.
    @type instrument: L{CompositeInstrument} or L{Instrument}

    @ivar sample: This variable contains the sample information.
    @type sample: L{Sample}
    """
    
    def __init__(self, **kwargs):
        """
        Object constructor
        
        @param kwargs: A list of key word arguments that the function accepts
        
        @keyword instrument: The instrument for the C{AttributeList} to hold
        @type instrument:  L{CompositeInstrument} or L{Instrument}
        
        @keyword sample: The sample for the C{AttributeList} to hold
        @type sample: L{Sample}
        """
        try:
            self.instrument = kwargs["instrument"]
        except KeyError:
            self.instrument = None

        try:
            self.sample = kwargs["sample"]
        except KeyError:
            self.sample = None

    def __eq__(self, other):
        """
        This method checks to see if the incoming C{AttributeList} object and
        the current one are equal.

        @param other: Object to check for equality
        @type other: C{AttributeList}


        @return: I{True} if the C{AttributeList} objects are equal, I{False}
                 if they are not
        @rtype: C{boolean}
        """        
        try:

            if self.instrument != other.instrument:
                return False

            if self.sample != other.sample:
                return False

        except:
            return False

        return True

    def __ne__(self, other):
        """
        This method checks to see if the incoming C{AttributeList} object and
        the current one are not equal.

        @param other: Object to check for equality
        @type other: C{AttributeList}


        @return: I{True} if the C{AttributeList} objects are not equal,
                 I{False} if they are
        @rtype: C{boolean}
        """        
        return not self.__eq__(other)
