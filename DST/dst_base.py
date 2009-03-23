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

class DST_BASE:
    """
    This is the C{DST_BASE} abstract base class. It serves as the foundation
    for objects that handle data input and output. All concrete classes must
    override the constructor and the
    L{release_resource<DST_BASE.release_resource>} methods. All other methods
    are optional. 
    """
    
    # ----- initialization
    def __init__(self, resource):
        """
        Object constructor. ALL INHERITED OBJECTS MUST OVERRIDE.
        """
        raise NotImplementedError

    # ----- explicit close
    def release_resource(self):
        """
        Resource cleanup handler. ALL INHERITED OBJECTS MUST OVERRIDE.
        """
        raise NotImplementedError

    # ----- configuration

    # ----- inspection
    def get_SO_ids(self, som_id):
        """
        Method to get L{SOM.SO} IDs. INHERITED OBJECTS MAY OVERRIDE.
        """
        raise NotImplementedError

    def get_SOM_ids(self):
        """
        Method to get L{SOM.SOM} IDs. INHERITED OBJECTS MAY OVERRIDE.
        """
        raise NotImplementedError

    # ----- read information
    def getSO(self, som_id, so_id):
        """
        Retrieve a L{SOM.SO} from given L{SOM.SOM} and L{SOM.SO} IDs.
        INHERITED OBJECTS MAY OVERRIDE.
        """
        raise NotImplementedError

    def getSOM(self, som_id):
        """
        Retrieve a L{SOM.SOM} for a given L{SOM.SOM} ID.
        INHERITED OBJECTS MAY OVERRIDE.
        """        
        raise NotImplementedError

    # ----- write information
    def writeSO(self, so):
        """
        Method to write the L{SOM.SO} information to the resource.
        INHERITED OBJECTS MAY OVERRIDE.
        """
        raise NotImplementedError

    def writeSOM(self, som):
        """
        Method to write the L{SOM.SOM} information to the resource.
        INHERITED OBJECTS MAY OVERRIDE.
        """        
        raise NotImplementedError

def getInstance(mime_type, resource, *args, **kwargs):
    """
    Static factory method to create a concrete L{DST_BASE} class.

    @param mime_type: The MIME_TYPE that identifies the particular concrete
    DST instance one wants to instantiate. The currently accepted values are
       - text/Spec
       - text/Dave2d
       - application/x-NeXus
       - application/x-NxsGeom
       - text/rmd
       - text/num-info
       - text/GSAS
       - text/PHX
    @type mime_type: C{string}

    @param resource: A handle to the file resource
    @type resource: C{file}

    @param args: Arguments that the requested concrete DST class will accept
    @type args: Various arguments

    @param kwargs: A list of keyword arguments that the requested concrete
                   DST class will accept


    @return: A concrete DST instance
    @rtype: Concrete L{DST_BASE}


    @raise Exception: The mime-type does not correspond to an allowed DST
    """
    # prepare the arguments
    my_args = [resource]
    my_args.extend(args)

    # import the appropriate concrete classes
    import ascii3col_dst
    import dave2d_dst
    import geom_dst
    import gsas_dst
    import mdw_dst
    import nexus_dst
    import numinfo_dst
    import phx_dst

    # do the factory stuff
    if mime_type == nexus_dst.NeXusDST.MIME_TYPE:
        return nexus_dst.NeXusDST(*my_args, **kwargs)
    elif mime_type == ascii3col_dst.Ascii3ColDST.MIME_TYPE:
        return ascii3col_dst.Ascii3ColDST(*my_args, **kwargs)
    elif mime_type == dave2d_dst.Dave2dDST.MIME_TYPE:
        return dave2d_dst.Dave2dDST(*my_args, **kwargs)
    elif mime_type == gsas_dst.GsasDST.MIME_TYPE:
        return gsas_dst.GsasDST(*my_args, **kwargs)
    elif mime_type == geom_dst.GeomDST.MIME_TYPE:
        return geom_dst.GeomDST(*my_args, **kwargs)
    elif mime_type == mdw_dst.MdwDST.MIME_TYPE:
        return mdw_dst.MdwDST(*my_args, **kwargs)
    elif mime_type == numinfo_dst.NumInfoDST.MIME_TYPE:
        return numinfo_dst.NumInfoDST(*my_args, **kwargs)
    elif mime_type == phx_dst.PhxDST.MIME_TYPE:
        return phx_dst.PhxDST(*my_args, **kwargs)    
    else:
        raise Exception("Cannot create DST for type %s" % mime_type)
