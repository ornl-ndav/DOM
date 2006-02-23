class DST_BASE:
    
    def __init__(self):
        pass
        
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
