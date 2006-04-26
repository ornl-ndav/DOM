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
    import nexus_dst

    # do the factory stuff
    if mime_type==nexus_dst.NeXusDST.MIME_TYPE:
        return apply(nexus_dst.NeXusDST,my_args,kwargs)
    elif mime_type==ascii3col_dst.Ascii3ColDST.MIME_TYPE:
        return apply(ascii3col_dst.Ascii3ColDST,my_args,kwargs)
    elif mime_type==dave2d_dst.Dave2dDST.MIME_TYPE:
        return apply(dave2d_dst.Dave2dDST,my_args,kwargs)
    else:
        raise Exception,"something wrong"
