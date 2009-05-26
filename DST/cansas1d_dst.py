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

import dst_base
import lxml.etree as le

class CanSas1dDST(dst_base.DST_BASE):
    """
    This class creates a CanSAS 1D format file. This file is based on the
    schema specification found U{here<>}.

    @cvar MIME_TYPE: The MIME-TYPE of the class
    @type MIME_TYPE: C{string}

    @ivar __file: The handle to the output data file
    @type __file: C{file}

    """
    MIME_TYPE = "text/canSAS"

    ########## DST_BASE functions

    def __init__(self, resource, *args, **kwargs):
        """
        Object constructor

        @param resource: The handle to the output data file
        @type resource: C{file}

        @param args: Argument objects that the class accepts (UNUSED)

        @param kwargs: A list of keyword arguments that the class accepts:
        """

        self.__file = resource

    def release_resource(self):
        """
        This method closes the file handle to the output file.
        """
        self.__file.close()

    def writeSOM(self, som):
        """
        This method writes the L{SOM.SOM} information to the output file.

        @param som: The object to have its information written to file.
        @type som: L{SOM.SOM}
        """
        # CanSAS front matter
        CANSAS_VERSION = "1.0"
        CANSAS_NS = "cansas1d/" + CANSAS_VERSION
        CANSAS_XSD_LOC = CANSAS_NS + " " + \
        "http://svn.smallangles.net/svn/canSAS/1dwg/trunk/cansas1d.xsd"

        NSMAP = {None : CANSAS_NS,
                 "xsi" : "http://www.w3.org/2001/XMLSchema-instance"}

        xsd_location = '{%s}schemaLocation' % NSMAP["xsi"]
        
        root = le.Element("SASroot", nsmap=NSMAP,
                          attrib={"version" : CANSAS_VERSION,
                                  xsd_location : CANSAS_XSD_LOC})

        entry = le.SubElement(root, "SASentry")

        title = le.SubElement(entry, "Title")
        title.text = som.attr_list["data-title"]
        run_numbers = som.attr_list["data-run_number"].split('/')
        for run_number in run_numbers:
            run = le.SubElement(entry, "Run")
            run.text = run_number.strip()

        data = le.SubElement(entry, "SASdata")

        bin_centers = som[0].axis[0].val.toNumPy(True)

        import math
        for i, bin_center in enumerate(bin_centers):
            idata = le.SubElement(data, "Idata")
            Q = le.SubElement(idata, "Q",
                              attrib={"unit" : som.getAxisUnits(0)})
            Q.text = str(som[0].axis[0].val[i])
            I = le.SubElement(idata, "I",
                              attrib={"unit" : som.getYUnits()})
            I.text = str(som[0].y[i])
            Idev = le.SubElement(idata, "Idev",
                                 attrib={"unit" : som.getYUnits()})
            Idev.text = str(math.sqrt(som[0].var_y[i]))

        sample = le.SubElement(entry, "SASsample")
        sample_id = le.SubElement(sample, "ID")
        sample_id.text = som.attr_list.sample.name

        inst = le.SubElement(entry, "SASinstrument")
        inst_name = le.SubElement(inst, "name")
        inst_name.text = som.attr_list.instrument.get_name()

        source = le.SubElement(inst, "SASsource")
        radiation = le.SubElement(source, "radiation")
        radiation.text = "neutron"

        collimation = le.SubElement(inst, "SAScollimation")

        detector = le.SubElement(inst, "SASdetector")
        det_name = le.SubElement(detector, "name")
        if som.attr_list.instrument.get_name() == "EQSANS":
            det_name.text = "He3 LPSD"
        elif som.attr_list.instrument.get_name() == "SANS":
            det_name.text = "ORDELA"
        else:
            raise RuntimeError("Do not understand instrument %s" %\
                               som.attr_list.instrument.get_name())

        det_sdd = le.SubElement(detector, "SDD", attrib={"unit" : "m"})
        det_sdd.text = str(som.attr_list.instrument.get_det_secondary()[0])
        
        note = le.SubElement(entry, "SASnote")

        self.__file.write(le.tostring(root, pretty_print=True,
                                      xml_declaration=True))
        
