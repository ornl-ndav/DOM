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

class MdwDST(dst_base.DST_BASE):
    """
    This class creates a XML metadata file from the C{hlr_utils.Configuration}
    object which records the setup of a particular pass of data reduction.

    @cvar MIME_TYPE: The MIME-TYPE of the class
    @type MIME_TYPE: C{string}
    
    @cvar EMPTY: Variable for holding an empty string
    @type EMPTY: C{string}
    
    @cvar SPACE: Variable for holding a space
    @type SPACE: C{string}

    @ivar __file: The handle to the output data file
    @type __file: C{file}

    @ivar __doc: The handle to the XML document object
    @type __doc: C{xml.dom.minidom.Document}
    """
    
    MIME_TYPE = "text/rmd"
    EMPTY = ""
    SPACE = " "

    ########## DST_BASE functions

    def __init__(self, resource, *args, **kwargs):
        """
        Object constructor

        @param resource: The handle to the output data file
        @type resource: C{file}

        @param args: Argument objects that the class accepts (UNUSED)

        @param kwargs: A list of keyword arguments that the class accepts:
        """        
        import xml.dom.minidom
        
        self.__file = resource
        self.__doc = xml.dom.minidom.Document()

    def release_resource(self):
        """
        This method closes the file handle to the output file.
        """        
        self.__file.close()

    def writeSOM(self, som):
        """
        This method writes the L{SOM.SOM} information to the output file. In
        this case, a C{hlr_utils.Configuration} object is being searched for.
        If one is not present, an empty XML file will be written.

        @param som: The object to have its information written to file.
        @type som: L{SOM.SOM}
        """
        try:
            self.writeConfig(som.attr_list["config"])
        except KeyError:
            pass

        self.writeFile()
        
    ########## Special functions

    def writeConfig(self, config):
        """
        This method writes the information contained in the
        C{hlr_utils.Configuration} object into the XML document object.

        @param config: The object containing the data reduction setup
                       information.
        @type config: C{hlr_utils.Configuration}
        """
        mainnode = self.__doc.createElement("config")
        self.__doc.appendChild(mainnode)

        for key, value in config.__dict__.items():

            if value is not False and value is not None:
                snode = self.__doc.createElement(key)
                stype = str(type(value)).split('\'')[1]
                snode.setAttribute("type", stype)
                try:
                    snode = value.toXmlConfig(self.__doc, snode)
                except AttributeError:
                    tnode = self.__doc.createTextNode(str(value))
                    snode.appendChild(tnode)

                mainnode.appendChild(snode)
            else:
                pass

    def writeFile(self):
        """
        This method writes the XML document to the attached output file.
        """
        import xml.dom.ext

        xml.dom.ext.PrettyPrint(self.__doc, self.__file)
