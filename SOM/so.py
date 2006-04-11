import nessi_list

class SO:

    def __init__(self,dim=1,id=None,**kwargs):

        self.y     = nessi_list.NessiList()
        self.var_y = nessi_list.NessiList()
        self.id    = id
        self.axis = []
        for i in range(dim):
            self.axis.append(PrimaryAxis(i+1,**kwargs))

    def dim(self):
        return len(self.axis)

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

    def __eq__(self,other):
        try:
            if len(self.y) != len(other.y):
                return False

            if len(self.var_y) != len(self.var_y):
                return False

            if len(self.axis) != len(other.axis):
                return False

            for axis_self,axis_other in map(None,self.axis,other.axis):
                if axis_self != axis_other:
                    return False

        except:
            return False

        return True

    def __ne__(self,other):
        return not self.__eq__(other)


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

    def __eq__(self,other):
        try:
            if len(self.val) != len(other.val):
                return False

            if(self.var != None):
                if len(self.var) != len(self.var):
                   return False

        except:
            return False

        return True

    def __ne__(self,other):
        return not self.__eq__(other)
    
        
if __name__ == "__main__":
    so1 = SO(withVar=True)
    so1.axis[0].val.extend([1.0,2.0,3.0])
    so1.axis[0].var.extend([1.0,2.0,3.0])
    so1.y.extend([40.0,55.0])
    so1.var_y.extend([40.0,55.0])
    so1.id="Pixel 1"
    print "1D SO:", so1

    so2 = SO(withVar=True)
    so2.axis[0].val.extend([1.0,2.0,3.0])
    so2.axis[0].var.extend([1.0,2.0,3.0])
    so2.y.extend([60.0,65.0])
    so2.var_y.extend([60.0,65.0])
    so2.id="Pixel 2"
    print "1D SO:", so2

    if so1 == so2:
        print "Is equals"
    else:
        print "Not equal"
