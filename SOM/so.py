import nessi_list

class SO:

    def __init__(self):
        self.x     = nessi_list.NessiList(0)
        self.y     = nessi_list.NessiList(0)
        self.var_y = nessi_list.NessiList(0)
        self.id    = None

    def __len__(self):
        return len(self.y)
