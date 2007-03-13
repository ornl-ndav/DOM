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
import dst_utils
import math

class NumInfoDST(dst_base.DST_BASE):
    MIME_TYPE="text/num-info"
    EMPTY=""
    SPACE=" "

    ########## DST_BASE functions

    def __init__(self, resource, attr_name, *args, **kwargs):
        import time
        import xml.dom.minidom

        self.__attr_name = attr_name
        self.__doc = xml.dom.minidom.Document()
        self.__file = resource
        self.__timestamp = dst_utils.make_ISO8601(time.time())
        
    def release_resource(self):
        self.__file.close()

    def writeSOM(self,som):
        self.prepareContents(som)
        self.writeFile()

    ########## Special functions

    def prepareContents(self, som):

        try:
            num_list = som.attr_list[self.__attr_name]
        except KeyError:
            raise RuntimeError("Attribute %s is not present in SOM" \
                               % self.__attr_name)

        num_list_size = len(num_list)
        som_size = len(som)

        if num_list_size != som_size:
            raise RuntimeError("Numeric information and SOM do not have the "\
                               +"same number of entries.")

        values = [num_list[i][0] for i in xrange(num_list_size)]
        errors = [math.sqrt(num_list[i][1]) for i in xrange(num_list_size)]
        ids = [som[i].id for i in xrange(som_size)]

        value_string_bank_list = []
        error_string_bank_list = []
        bank_list = []

        bank_check = True
        bank_id = ids[0][0]
        bank_list.append(bank_id)
        line_count = 8
        counter = 1

        import os
        
        value_substring = []
        value_bank_string = os.linesep
        error_substring = []
        error_bank_string = os.linesep

        make_substring = False
        
        for j in xrange(som_size):
            if bank_id == ids[j][0]:
                pass
            else:
                value_bank_string += " ".join(value_substring)+os.linesep
                value_string_bank_list.append(value_bank_string)
                error_bank_string += " ".join(error_substring)+os.linesep
                error_string_bank_list.append(error_bank_string)

                bank_id = ids[j][0]
                bank_list.append(bank_id)
                counter = 1
                value_substring = []
                value_bank_string = os.linesep
                error_substring = []
                error_bank_string = os.linesep                
                
            if counter == line_count:
                counter = 1
                value_bank_string += " ".join(value_substring)+os.linesep
                value_substring = []
                error_bank_string += " ".join(error_substring)+os.linesep
                error_substring = []
                make_substring = True
            else:
                pass

            value_substring.append("%.3f" % values[j])
            error_substring.append("%.3f" % errors[j])
            counter += 1                

        value_bank_string += " ".join(value_substring)+os.linesep
        error_bank_string += " ".join(error_substring)+os.linesep
        value_string_bank_list.append(value_bank_string)
        error_string_bank_list.append(error_bank_string)
        
        mainnode = self.__doc.createElement(self.__attr_name)
        mainnode.setAttribute("created", self.__timestamp)

        for k in range(len(value_string_bank_list)):
            banknode = self.__doc.createElement(bank_list[k])
            valuenode = self.__doc.createElement("value")
            valuetnode = self.__doc.createTextNode(value_string_bank_list[k])
            valuenode.appendChild(valuetnode)
            errornode = self.__doc.createElement("error")
            errortnode = self.__doc.createTextNode(error_string_bank_list[k])
            errornode.appendChild(errortnode)
            banknode.appendChild(valuenode)
            banknode.appendChild(errornode)
            mainnode.appendChild(banknode)

        self.__doc.appendChild(mainnode)        

    def writeFile(self):
        import xml.dom.ext

        xml.dom.ext.PrettyPrint(self.__doc, self.__file)
