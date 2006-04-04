import nessi_list

class SO_Base:

    def __init__(self,id=None):

        if self.__class__ == SO_Base:
            raise NotImplementedError, "Cannot instantiate a SO_Base object"
        
        self.y     = nessi_list.NessiList()
        self.var_y = nessi_list.NessiList()
        self.id    = id
        self.x     = None

    def __len__(self):
        return len(self.y)

    def __str__(self):
        if self.id == None:
            return "(None, "+str(self.x)+", "+str(self.y)+\
                   ", "+str(self.var_y)+")"
        else:
            return "("+str(self.id)+", "+str(self.x)+", "+str(self.y)+\
                   ", "+str(self.var_y)+")"

    def __repr__(self):
        return self.__str__()


class PrimaryAxis:
    
    def __init__(self,id=1,**kwargs):
        
        self.x = nessi_list.NessiList()
        if kwargs.has_key("withVar"):
            self.var_x = nessi_list.NessiList()
        else:
            self.var_x = None
        self.xid = id

    def __len__(self):
        return len(self.x)

    def __str__(self):
        if self.var_x==None:
            return "("+str(self.xid)+", "+str(self.x)+")"
        else:
            return "("+str(self.xid)+", "+str(self.x)+", "+str(self.var_x)+")"

    def __repr__(self):
        return self.__str__()


class SO( SO_Base ):
    
    def __init__(self,dim=1,**kwargs):
        
        SO_Base.__init__(self)
        self.x = []
        for i in range(dim):
            self.x.append(PrimaryAxis(i+1,**kwargs))

        
    
