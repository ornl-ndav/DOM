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
import optparse
from SOM import SOM
from SOM import SO
from time import localtime, strftime, time

parser = optparse.OptionParser(usage="usage: %prog [options]")

parser.add_option("", "--with-xvar", action="store_true", dest="withXvar",
                  help="Create SOs with variances on x axis")
parser.set_defaults(withXvar=False)

parser.add_option("", "--extra-som", action="store_true", dest="extraSom",
                  help="Create another SOM for an extra column")
parser.set_defaults(extraSom=False)

(options, args) =  parser.parse_args()

filename_SOM1 = "stuff1.dat"

SOM1 = SOM()
SOM1.attr_list["filename"] = filename_SOM1
SOM1.attr_list["username"] = "Michael Reuter and the Gang"
SOM1.setAllAxisLabels(["TOF"])
SOM1.setAllAxisUnits(["microseconds"])
SOM1.setYLabel("Counts")
SOM1.setYUnits("counts")
SOM1.setDataSetType("histogram")

if options.extraSom:
    SOM2 = SOM()
    SOM2.copyAttributes(SOM1)
    SOM2.setAllAxisLabels(["Wavelength"])
    SOM2.setAllAxisUnits(["Angstroms"])
    SOM2.setYLabel("Counts")
    SOM2.setYUnits("counts")
    SOM2.setDataSetType("histogram")
else:
    SOM2 = None

for i in range(2):
    SO1 = SO(construct=True, withVar=options.withXvar)
    if options.extraSom:
        SO2 = SO(construct=True)
    for j in range(10):
        SO1.id = i
        SO1.axis[0].val.append(j+1)
        if options.withXvar:
            SO1.axis[0].var.append(j+1)
        SO1.y.append(1000+j+(20*j))
        SO1.var_y.append(100+j)
        if options.extraSom:
            SO2.id = i
            SO2.axis[0].val.append((j+1)*1.0579838)
            SO2.y.append(1000+j+(20*j))
            SO2.var_y.append(100+j)
        
    SO1.axis[0].val.append(11)
    if options.withXvar:
        SO1.axis[0].var.append(11)

    if options.extraSom:
        SO2.axis[0].val.append(11*1.0579838)
    
    SOM1.append(SO1)
    if options.extraSom:
        SOM2.append(SO2)

file = open(filename_SOM1, "w")

a3c = DST.Ascii3ColDST(file)
a3c.writeSOM(SOM1, extra_som=SOM2)
a3c.release_resource()


