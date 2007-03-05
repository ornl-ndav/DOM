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

###############################################################################
#
# This class creates a XML metadata file from the Configuration object
#
# $Id$
#
###############################################################################

import dst_base

class MdwDST(dst_base.DST_BASE):
    MIME_TYPE="text/rmd"
    EMPTY=""
    SPACE=" "

    ########## DST_BASE functions

    def __init__(self, resource, *args, **kwargs):

        import xml.dom.minidom
        
        self.__file = resource
        self.__doc = xml.dom.minidom.Document()

    def release_resource(self):
        self.__file.close()

    def writeSOM(self,som):
        try:
            self.writeConfig(som.attr_list["config"])
        except KeyError:
            pass

        self.writeFile()
        
    ########## Special functions

    def writeConfig(self, config):

        mainnode = self.__doc.createElement("config")
        self.__doc.appendChild(mainnode)

        for key, value in config.__dict__.items():

            if value is not False and value is not None:
                snode = self.__doc.createElement(key)
                tnode = self.__doc.createTextNode(str(value))
                snode.appendChild(tnode)
                mainnode.appendChild(snode)
            else:
                pass

    def writeFile(self):
        import xml.dom.ext

        xml.dom.ext.PrettyPrint(self.__doc, self.__file)
