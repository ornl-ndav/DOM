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

    def __init__(self, resource, *args, **kwargs):
        import time
        import xml.dom.minidom

        self.__doc = xml.dom.minidom.Document()
        self.__file = resource
        self.__epoch = time.time()

        try:
            self.__line_wrap_num = kwargs["line_wrap_num"]
        except KeyError:
            self.__line_wrap_num = 4

        try:
            self.__tag = kwargs["tag"]
        except KeyError:
            self.__tag = "Integral"

        try:
            self.__units = kwargs["units"]
        except KeyError:
            self.__units = "counts"

        try:
            self.__comments = kwargs["comments"]
        except KeyError:
            self.__comments = None
        
    def release_resource(self):
        self.__file.close()

    def writeSO(self,so):
        self.writeData(so)

    def writeSOM(self,som):
        dst_utils.write_spec_header(self.__file, self.__epoch, som)

        if self.__comments is not None:
            for comment in self.__comments:
                print >> self.__file, "#C", comment
 	       
        print >> self.__file, \
              "#L Pixel ID  %s (%s) Error (%s)" % (self.__tag, self.__units,
                                                   self.__units)
        for so in som:
            self.writeData(so)
        
        #self.prepareContents(som)
        #self.writeFile()

    ########## Special functions

    def writeData(self, so):
        try:
            variance = math.sqrt(so.var_y)
        except OverflowError:
            variance = float('inf')
        
        print >> self.__file, so.id, so.y, variance

    def prepareContents(self, som):
        self.__parseContentsForXml(values, errors, ids)

    def __parseContentsForXml(self, values, errors, ids):
        # NOT VALID, NEEDS TO BE REDONE IF XML IS DESIRED
        value_string_bank_list = []
        error_string_bank_list = []
        bank_list = []

        bank_check = True
        bank_id = ids[0][0]
        bank_list.append(bank_id)
        counter = 0

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
                counter = 0
                value_substring = []
                value_bank_string = os.linesep
                error_substring = []
                error_bank_string = os.linesep                
                
            if counter == self.__line_wrap_num:
                counter = 0
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
        mainnode.setAttribute("created", dst_utils.makeIS08601(self.__epoch))

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

    
