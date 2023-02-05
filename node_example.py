class Node:

    def __init__(self,parent = None):
        self.parent = parent
        self.children = []
        self.child_index = None

    def AddNode(self):
        new_child = Node(self)
        self.children.append(new_child)
        new_child.child_index = self.children.index(new_child)
        return new_child

    def getIndex(self):
        return self.child_index

a = Node()
b = a.AddNode()
c = a.AddNode()
d = a.AddNode()

print d.getIndex()
print c.getIndex()
print b.getIndex()