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
import SOM
import hlr_utils

filename = "numinfo.xml"
tagname = "normalization_efficiency"

som = SOM.SOM()
so1 = SOM.SO()
so1.id = ("bank1", (0, 0))
som.append(so1)
so2 = SOM.SO()
so2.id = ("bank2", (0, 0))
som.append(so2)

num_list = [(111.0, 23.0), (143.0, 27.0)]
som.attr_list[tagname] = num_list

ofile = open(filename, "w")

nif = DST.NumInfoDST(ofile, tagname)
nif.writeSOM(som)
nif.release_resource()
