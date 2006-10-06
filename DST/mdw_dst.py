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
