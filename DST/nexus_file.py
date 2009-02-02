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

import sns_napi
import enum

class NeXusError(SystemError):
    pass

class NeXusFile:
    # access methods
    ACCESS = enum.Enum()
    ACCESS.set("READ",      sns_napi.ACC_READ)
    ACCESS.set("RDWR",      sns_napi.ACC_RDWR)
    ACCESS.set("CREATE",    sns_napi.ACC_CREATE)
    ACCESS.set("CREATE4",   sns_napi.ACC_CREATE4)
    ACCESS.set("CREATE5",   sns_napi.ACC_CREATE5)
    ACCESS.set("CREATEXML", sns_napi.ACC_CREATEXML)
    ACCESS.set("NOSTRIP",   sns_napi.ACC_NOSTRIP)

    # ----- python stuff
    def __init__(self, filename, access=sns_napi.ACC_READ):
        self.__HANDLE__ = sns_napi.open(filename, access)
        if self.__HANDLE__ is None:
            raise SystemError("Failed to read file: %s" % filename)
        self.__filename    = filename
        self.__path        = []
        self.__dataopen    = False

    def filename(self):
        return self.__filename

    def getselfpath(self):
        return self.__path

    # ----- napi stuff
    def flush(self):
        sns_napi.flush(self.__HANDLE__)

    def makegroup(self, name, type):
        return sns_napi.makegroup(self.__HANDLE__, name, type)

    def opengroup(self, name, type):
        self.__path.append(name)
        return sns_napi.opengroup(self.__HANDLE__, name, type)

    def openpath(self, path):
        #print "\n"
        #print "=== %s" % path
        #print self.__path
        
        if self.__path != []:
            if path == self.__path[-1]:
                #print "We are here already"
                return
        
        # This next case is when we are asked for a data item alone, and we are already have
        # a data item open.  Otherwise it will do a groupdir and find the new item and just
        # try to open it!
        if self.__dataopen and path.find("/") == -1:
            self.closedata()
        
        if path == "/":
            destination = []
        elif path.startswith("/"):
            destination = path[1:].split("/")
        else:
            destination = self.__path + path.split("/")
    
        temp = []
        # Now lets deal with any "." or ".." 
        for item in destination:
                if item == ".":
                    # Don't bother adding it.
                    pass
                elif item == "..":
                    if temp != []:
                        # go up a directory
                        temp.pop()
                    else:
                        raise NeXusError("You can't go further up the tree than the top!")
                else:
                    temp.append(item)
        
        destination = temp
        #print "current path",self.__path
        #print "%s"%path,destination
        
        up = []
        down = []
        
        for i, name in enumerate(destination):
            if i == len(self.__path):
                # destination is longer than current dir
                up = []
                down = destination[i:]
                break
            elif self.__path[i] != name:
                up = self.__path[i:]
                down = destination[i:]
                break
            else:
                up = self.__path[len(destination):]
                down = []
                
        up.reverse()
        
        #print "close,open",up,down
        
        # Close stuff on the way up
        if self.__dataopen and up != []:
            # Data item is open and we actually want to move!
            #print "closedata(%s)" % up[0]
            self.closedata()
            up.pop(0)
        for dir in up:
            #print up.index(dir)
            #print "closegroup(%s)" % dir
            self.closegroup()
                        
        # Open stuff on the way down.
        for dir in down:
            #print "looking for %s" % dir
            name = "crap.py :-)"
            self.initgroupdir()
            while name is not None:
                (name,classname) = self.getnextentry()
                #print name,dir
                if name != dir: continue
                if classname != "SDS":
                    #print "opengroup(%s)" % name
                    self.opengroup(name, classname)
                else:
                    #print "opendata(%s)" % name
                    self.opendata(name)
                
    def opengrouppath(self, path):
        #self.__path = ""
        return sns_napi.opengrouppath(self.__HANDLE__, path)
        
    def closegroup(self):
        self.__path.pop()
        return sns_napi.closegroup(self.__HANDLE__)

    def makedata(self, name, type, dims):
        return sns_napi.makedata(self.__HANDLE__, name, type, dims)

    def compmakedata(self, name, type, dims, c_buffer):
        return sns_napi.compmakedata(self.__HANDLE__, name, type, dims)

    def compress(self, compression):
        return sns_napi.compress(self.__HANDLE__, compression)

    def opendata(self, name):
        self.__path.append(name)
        self.__dataopen = True
        return sns_napi.opendata(self.__HANDLE__, name)

    def closedata(self):
        self.__path.pop()
        self.__dataopen = False
        return sns_napi.closedata(self.__HANDLE__)

    def putdata(self, c_ptr):
        return sns_napi.putdata(self.__HANDLE__, c_ptr)

    def putslab(self, c_ptr, dims):
        return sns_napi.putslab(self.__HANDLE__, c_ptr, dims)

    def getdata(self, type="f"):
        return sns_napi.getdata(self.__HANDLE__, type)

    def getslab(self, start, size, type="f"):
        return sns_napi.getslab(self.__HANDLE__, start, size, type)

    def putattr(self, name, c_ptr, type):
        return sns_napi.putattr(self.__HANDLE__, name, c_ptr, type)

    def getdataID(self):
        return sns_napi.getdataID(self.__HANDLE__)

    def makelink(self, link):
        return sns_napi.makelink(self.__HANDLE__, link)

    def opensourcegroup(self):
        #self.__path = ""
        return sns_napi.opensourcegroup(self.__HANDLE__)

    def getdims(self):
        return sns_napi.getinfo(self.__HANDLE__)

    def getnextentry(self):
        (name, nxclass, number) = sns_napi.getnextentry(self.__HANDLE__)
        return (name, nxclass)

    def getnextattr(self):
        return sns_napi.getnextattr(self.__HANDLE__)

    def getattr(self, name, type):
        return sns_napi.getattr(self.__HANDLE__, name)

    def getgroupID(self):
        return sns_napi.getgroupID(self.__HANDLE__)

#    def sameID(self): # not exposed through swig
#        raise NotImplementedError

    def initgroupdir(self):
        return sns_napi.initgroupdir(self.__HANDLE__)

    def initattrdir(self):
        return sns_napi.initattrdir(self.__HANDLE__)

#    def setnumberformat(self): # not exposed through swig
#        raise NotImplementedError

##### These two functions appear in napi.h, but should NEVER be
##### brought into the python layer
#extern  NXstatus  NXmalloc(void** data, int rank, int dimensions[],
# int datatype);
#extern  NXstatus  NXfree(void** data);
