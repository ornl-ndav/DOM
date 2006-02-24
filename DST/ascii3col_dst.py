###############################################################################
#
# This class creates a 3 column ASCII file with a metadata header. The
# formatting is based on spec
# (http://www.certif.com/spec_manual/user_1_4_1.html) file format.
#
# $Id$
#
###############################################################################

import dst_base

class Ascii3ColDST(dst_base.DST_BASE):
    MIME_TYPE="text/Spec"

    ########## DST_BASE functions

    def __init__(self, resource, *args, **kwargs):
        self.__file = resource


    def release_resource(self):
        self.__file.close()


    def writeSO(self,so):
        self.__so = so
        writeData()


    def writeSOM(self,som):
        self.__som = som
        writeHeader()
        writeData()

    ########## Special functions

    def writeHeader(self):
        raise NotImplementedError


    def writeData(self):
        raise NotImplementedError
        
