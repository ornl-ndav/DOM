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

class AttributeList(dict):
    def __init__(self,**kwargs):
        """
        Parameters:
        -----------
        ->kwargs is a list of key word arguments that the function accepts:
             instrument = the instrument for the AttributeList to hold
             sample     = the sample for the AttributeList to hold
        """

        try:
            self.instrument=kwargs["instrument"]
        except KeyError:
            self.instrument=None

        try:
            self.sample=kwargs["sample"]
        except KeyError:
            self.sample=None


    def __eq__(self, other):
        try:

            if self.instrument != other.instrument:
                return False

            if self.sample != other.sample:
                return False

        except:
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)
