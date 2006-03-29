import nessi_list

class SO:

    def __init__(self):
        self.x     = nessi_list.NessiList()
        self.y     = nessi_list.NessiList()
        self.var_x = None
        self.var_y = nessi_list.NessiList()
        self.id    = None

    def __len__(self):
        return len(self.y)

    def __str__(self):
        if self.var_x==None:
            return "("+str(self.id)+", "+str(self.x)+", "+str(self.y)+\
                   ", "+str(self.var_y)+")"
        else:
            return "("+str(self.id)+", "+str(self.x)+", "+str(self.y)+\
                   ", "+str(self.var_x)+", "+str(self.var_y)+")"

    def __repr__(self):
        return self.__str__()


