import nxpython

class SNSNeXus:
    __ATTR      = "ATTR"
    __SDS       = "SDS"
    __SEPARATOR = ":"

    def __init__(self,filename,access=nxpython.NXACC_READ):
        if(access!=nxpython.NXACC_READ):
            raise NotImplementedError,"Can only read files"
        self.__HANDLE__=nxpython.nx_open(filename,access)
        if(self.__HANDLE__==None):
            raise SystemError,"Failed to read file: %s" % filename
        self.__filename    = filename
        self.__group_level = 0
        self.__in_data     = False

    def __del__(self):
        self.close_file()

    def filename(self):
        return self.__filename

    def close_file(self): 
        if(self.__HANDLE__!=None):
            nxpython.nx_close(self.__HANDLE__)
            self.__HANDLE__=None

    def __split_group(self,stuff):
        return stuff.split(SNSNeXus.__SEPARATOR) # (name,type,number)

    def open_level(self,name,type):
        if(type.startswith(SNSNeXus.__SDS)):
            if(nxpython.nx_opendata(self.__HANDLE__,name)!=1):
                raise SystemError,"Could not open data \"%s\"" % name
            self.__in_data=True
        else:
            if(nxpython.nx_opengroup(self.__HANDLE__,name,type)!=1):
                raise SystemError,"Could not open \"%s:%s\"" % (name,type)
            self.__group_level=self.__group_level+1

    def close_level(self):
        if(self.__in_data):
            if(nxpython.nx_closedata(self.__HANDLE)!=1):
                raise SystemError,"Could not close level"
            self.__in_data=False
        else:
            if(nxpython.nx_closegroup(self.__HANDLE__)!=1):
                raise SystemError,"Could not close level"
            self.__group_level=self.__group_level-1

    def close_to_root(self):
        while(self.__in_data or self.__group_level>0):
            self.close_level()

    def __format_type(self,type,number):
        if(type==SNSNeXus.__SDS or type==SNSNeXus.__ATTR):
            return type+number
        else:
            return type

    def __getnext(self):
        if(self.__in_data):
            attr=nxpython.nx_getnextattr(self.__HANDLE__,SNSNeXus.__SEPARATOR)
            if(attr==None):
                return (None,None)
            (name,type,length)=self.__split_group(attr)
            return (name,self.__format_type(SNSNeXus.__ATTR,length))
        else:
            entry=nxpython.nx_getnextentry(self.__HANDLE__,":")
            if(entry==None):
                return (None,None)
            (name,type,number)=self.__split_group(entry)
            return (name,self.__format_type(type,number))

        
    def ls(self):
        result={}

        nxpython.nx_initgroupdir(self.__HANDLE__)

        name="random string"
        while name!=None:
            (name,type)=self.__getnext()
            if(name!=None) and (not type.startswith("CDF0.0")):
                result[name]=type

        return result
