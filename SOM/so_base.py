import nessi_list

class SO_Base:

    def __init__(self,id=None):

        if self.__class__ == SO_Base:
            raise NotImplementedError, "Cannot instantiate a SO_Base object"
        
        self.y     = nessi_list.NessiList()
        self.var_y = nessi_list.NessiList()
        self.id    = id
        self.axis  = None

    def __len__(self):
        return len(self.y)

    def __str__(self):
        if self.id == None:
            return "(None, "+str(self.axis)+", "+str(self.y)+\
                   ", "+str(self.var_y)+")"
        else:
            return "("+str(self.id)+", "+str(self.axis)+", "+str(self.y)+\
                   ", "+str(self.var_y)+")"

    def __repr__(self):
        return self.__str__()


class PrimaryAxis:
    
    def __init__(self,id=1,**kwargs):
        
        self.val = nessi_list.NessiList()
        if kwargs.has_key("withVar"):
            self.var = nessi_list.NessiList()
        else:
            self.var = None
        self.pid = id

    def __len__(self):
        return len(self.val)

    def __str__(self):
        if self.var==None:
            return "("+str(self.pid)+", "+str(self.val)+")"
        else:
            return "("+str(self.pid)+", "+str(self.val)+", "\
                   +str(self.var)+")"

    def __repr__(self):
        return self.__str__()


class SO( SO_Base ):
    
    def __init__(self,dim=1,**kwargs):
        
        SO_Base.__init__(self)
        self.axis = []
        for i in range(dim):
            self.axis.append(PrimaryAxis(i+1,**kwargs))

        
if __name__ == "__main__":
    so1 = SO(withVar=True)
    so1.axis[0].val.extend([1.0,2.0,3.0])
    so1.axis[0].var.extend([1.0,2.0,3.0])
    so1.y.extend([40.0,55.0])
    so1.var_y.extend([40.0,55.0])
    so1.id="Pixel 1"
    print "1D SO:", so1
