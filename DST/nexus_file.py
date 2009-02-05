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

    def __getnxclass(self, name):
        """
        Return the nxclass of the supplied name.
        """
        self.initgroupdir()
        (myname, nxclass) = ("crap name","crap class")
        while (myname, nxclass) != (None, None):
            (myname, nxclass) = self.getnextentry()
            if myname == name:
                return nxclass
        return None

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
        """
        Open a particular group '/path/to/group'.  Paths can be
        absolute or relative to the currently open group.  If openpath
        fails, then currently open path may not be different from the
        starting path. For better performation the types can be
        specified as well using '/path:type1/to:type2/group:type3'
        which will prevent searching the file for the types associated
        with the supplied names.

        Raises ValueError.

        Corresponds to NXopenpath(handle, path)
        """
        self._openpath(path, opendata=True)

    def _openpath(self, path, opendata=True):
        """helper function: open relative path and maybe data"""
        
        if self.__path != []:
            if path == self.__path[-1]:
                #print "We are here already"
                return
        
        # Determine target node as sequence of group names
        if path == '/':
            target = []
        else:
            if path.endswith("/"):
                path = path[:-1]
            if path.startswith('/'):
                target = path[1:].split('/')
            else:
                target = self.__path + path.split('/')

        # Remove relative path indicators from target
        L = []
        for t in target: 
            if t == '.': 
                # Skip current node
                pass
            elif t == '..':
                if L == []:
                    raise ValueError("too many '..' in path")
                L.pop()
            else:
                L.append(t)
        target = L

        # split out nxclass from each level if available
        L = []
        for t in target:
            try:
                item = t.split(":")
                if len(item) == 1:
                    L.append((item[0], None))
                else:
                    L.append(tuple(item))
            except AttributeError:
                L.append(t)
        target = L

        #print "current path",self.__path
        #print "%s"%path,target

        # Find which groups need to be closed and opened
        up = []
        down = []
        #print "target is" ,target
        for (i, (name, nxclass)) in enumerate(target):
            
            #print i,name
            if i == len(self.__path):
                #print "target longer than current"
                up = []
                down = target[i:]
                break
            elif self.__path[i] != name:
                #print "target and current differ at",name
                up = self.__path[i:]
                down = target[i:]
                break
        else:
            #print "target shorter than current"
            up = self.__path[len(target):]
            down = []

        # add more information to the down path
        for i in xrange(len(down)):
            try:
                (name, nxclass) = down[i]
            except ValueError:
                down[i] = (down[i], None)
        #print "close,open",up,down

        # Close groups on the way up
        if self.__dataopen and up != []:
            #print "closedata(%s)" % up[-1]
            self.closedata()
            up.pop()
        for target in up:
            #print "closegroup(%s)" % target
            self.closegroup()
        
        # Open groups on the way down
        for (name, nxclass) in down:
            if nxclass is None:
                nxclass = self.__getnxclass(name)
                if nxclass is None:
                    raise IOError("Failed to find entry with name \"%s\"" \
                                   % name)
            if nxclass != "SDS":
                #print "opengroup(%s)" % name
                self.opengroup(name, nxclass)
            elif opendata:
                #print "opendata(%s)" % name
                self.opendata(name)
            else:
                raise IOError("node %s not in %s"%(name,self.path))

    def opengrouppath(self, path):
        """
        Open a particular group '/path/to/group', or the dataset containing
        the group if the path refers to a dataset.  Paths can be relative to
        the currently open group.

        Raises ValueError.

        Corresponds to NXopengrouppath(handle, path)
        """
        self._openpath(path,opendata=False)
        
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
        if self.__dataopen:
            self.closedata()
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
