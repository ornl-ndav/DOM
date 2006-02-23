import nxpython

class SNSNeXus:
    def __init__(self,filename,access=nxpython.NXACC_READ):
        self.__HANDLE__=nxpython.nx_open(filename,access)
        if(self.__HANDLE__==None):
            raise SystemError,"Failed to read file: %s" % filename
        self.__filename=filename

    def __del__(self):
        self.close()

    def filename(self):
        return self.__filename

    def close(self):
        if(self.__HANDLE__!=None):
            nxpython.nx_close(self.__HANDLE__)
            self.__HANDLE__=None

    def ls(self):
        result=[]
        # get the list of groups
        nxpython.nx_initgroupdir(self.__HANDLE__)
        entry=nxpython.nx_getnextentry(self.__HANDLE__,":")
        result.append(entry)
        while entry!=None:
            entry=nxpython.nx_getnextentry(self.__HANDLE__,":")
            result.append(entry)

        return result
