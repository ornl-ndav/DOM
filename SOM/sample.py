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

class Sample:
    """
    This is an abstract base class representing important information about
    the sample.

    @ivar name: The name of the sample
    @type name: C{string}

    @ivar nature: The type of sample
    @type nature: C{string}

    @ivar identifier: Serial number or other ID tagging scheme
    @type identifier: C{string}

    @ivar holder: The type of holder for the sample
    @type holder: C{string}

    @ivar changer_position: The location of the sample in a sample changer
    @type changer_position: C{string}
    """
    def __init__(self):
        """
        Object constructor
        """
        self.name = ""
        self.nature = ""
        self.identifier = ""
        self.holder = ""
        self.changer_position = ""
