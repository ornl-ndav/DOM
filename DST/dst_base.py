class DST_BASE:
    # ----- initialization
    def __init__(self,resource):
        raise NotImplementedError

    # ----- explicit close
    def release_resource(self):
        raise NotImpemetedError

    # ----- configuration

    # ----- inspection
    def num_avail_SO(self):
        raise NotImplementedError

    # ----- read information
    def getSO(self,id):
        raise NotImplementedError

    # ----- write information
    def writeSO(self,so):
        raise NotImplementedError

def getInstance(mime_type,resource,*args,**kwargs):
    # prepare the arguments
    my_args=[resource]
    my_args.extend(args)

    # import the appropriate concrete classes
    import nexus_dst

    # do the factory stuff
    if mime_type==nexus_dst.NeXusDST.MIME_TYPE:
        return apply(nexus_dst.NeXusDST,my_args,kwargs)
    else:
        raise Exception,"something wrong"
