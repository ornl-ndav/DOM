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
from SOM import SOM, SO, Sample, Instrument
from nessi_list import NessiList()

SOM1 = SOM()
SOM1.setDataSetType("histogram")
SOM1.setYLabel("Intensity")
SOM1.setYUnits("counts A / meV")
SOM1.SOM1.setAllAxisLabels(["momentum transfer", "energy transfer"])
SOM1.setAllAxisUnits(["1/A", "meV"])
SOM1.attr_list["data-title"] = "Test S(Q,E)"
SOM1.attr_list["data-run_number"] = "1344"

DSample = Sample()
DSample.name = "Test Sample"
DSample.nature = "CoCo"
SOM1.attr_list.sample = DSample

x = NessiList()
y = NessiList()
z = NessiList()

x.extend(0,1,2,3)
y.extend(0,1,2)
z.extend(1,2,3,4,5,6)

SO1 = SO(2)
SO1.id = ("bank1", (4, 32))
SO1.y = z
SO1.var_y = z
SO1.axis[0].var = x
SO1.axis[1].var = y

SOM1.append(SO1)

rednxs = DST.RedNxsDST("test_red.nxs")
rednxs.writeSOM(SOM1)
rednxs.release_resource()
