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

class DST_BASE:
    # ----- initialization
    def __init__(self,resource):
        raise NotImplementedError

    # ----- explicit close
    def release_resource(self):
        raise NotImplementedError

    # ----- configuration

    # ----- inspection
    def get_SO_ids(self,som_id):
        raise NotImplementedError

    def get_SOM_ids(self):
        raise NotImplementedError

    # ----- read information
    def getSO(self,som_id,so_id):
        raise NotImplementedError

    def getSOM(self,som_id):
        raise NotImplementedError

    # ----- write information
    def writeSO(self,so):
        raise NotImplementedError

    def writeSOM(self,som):
        raise NotImplementedError

def getInstance(mime_type,resource,*args,**kwargs):
    # prepare the arguments
    my_args=[resource]
    my_args.extend(args)

    # import the appropriate concrete classes
    import ascii3col_dst
    import dave2d_dst
    import geom_dst
    import gsas_dst
    import mdw_dst
    import nexus_dst

    # do the factory stuff
    if mime_type==nexus_dst.NeXusDST.MIME_TYPE:
        return apply(nexus_dst.NeXusDST,my_args,kwargs)
    elif mime_type==ascii3col_dst.Ascii3ColDST.MIME_TYPE:
        return apply(ascii3col_dst.Ascii3ColDST,my_args,kwargs)
    elif mime_type==dave2d_dst.Dave2dDST.MIME_TYPE:
        return apply(dave2d_dst.Dave2dDST,my_args,kwargs)
    elif mime_type==gsas_dst.GsasDST.MIME_TYPE:
        return apply(gsas_dst.GsasDST,my_args,kwargs)
    elif mime_type==geom_dst.GeomDST.MIME_TYPE:
        return apply(geom_dst.GeomDST,my_args,kwargs)
    elif mime_type==mdw_dst.MdwDST.MIME_TYPE:
        return apply(mdw_dst.MdwDST,my_args,kwargs)
    else:
        raise Exception,"something wrong"
