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

    def __init__(self, resource, *args, **kwargs):
        pass

