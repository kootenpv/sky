""" 

Update lxml object to contain:
- a set of children
- a set of parents
- depth 

"""

from lxml.etree import ElementTree

class Elhanced(lxml.etree._ElementTree):
    def __init__(self):
        super().__init__()
        self.parents = set()
        self.children = set()
        
    def categorize_nodes(self):
        it = 0
        queue = [self]
        while queue
        for node in self.iter():
            if node.get_children():
                self.parents.add(node)
            else:
                self.parents.add(node)
                    
        
        
    
