#!/usr/bin/env python

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

import DST
from SOM import SOM, SO

SOM1 = SOM()
SOM1.setDataSetType("histogram")
SOM1.setYLabel("Intensity")
SOM1.setYUnits("counts A")
SOM1.setAllAxisLabels(["Q"])
SOM1.setAllAxisUnits(["1/A"])

ifile = open("test_cansas1d.xml", "w")

cs1d = DST.CanSas1dDST(ifile)
cs1d.writeSOM(SOM1)
cs1d.release_resource()
