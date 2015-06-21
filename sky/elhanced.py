import lxml.html
import tempfile 
import webbrowser 
import time
from lxmlTree import lxmlTree
from helper import *

class ElhancedTree(): 
    def __init__(self, tree): 
        self.leafs = set()
        self.children = set()
        self.tree = tree
        self._reference = list(self.tree.iter()) 
        self.addDepth(self._reference[0])        
        
    def addDepth(self, node, depth = 0):
        tc = node.text_content()
        node.lenchars = len(tc) if tc else 0
        node.depth = depth
        node.isLeaf = False
        for n in node.iterchildren():
            if bool(list(n.iterchildren())): 
                self.addDepth(n, depth + 1)
            else:
                self.leafs.add(n)    
                tc = n.text_content()
                n.lenchars = len(tc) if tc else 0
                n.isLeaf = True

    def view(self, *args):
        lxmlTree(*args)

    def viewPage(self):
        with tempfile.NamedTemporaryFile('r+', suffix = '.html') as f:
            f.write(lxml.html.tostring(self.tree).decode('utf8'))
            f.flush()
            webbrowser.open('file://' + f.name) 
            time.sleep(1) 

    def compare(self, other):
        if isinstance(other, ElhancedTree):
            other = other.tree 
        lxmlTree([self.tree, other])
    


        
e1 = ElhancedTree(getQuickTree('http://www.nieuwsdumper.nl/nieuws/1454/eerste-volvo-fmx-410-8x4-tridem-betonmixer-voor-bck.html'))
e2 = ElhancedTree(getQuickTree('http://www.nieuwsdumper.nl/nieuws/1666/ihi-38n-voor-van-zuijlen.html'))

e1 = ElhancedTree(getQuickTree('http://www.bbc.com/news/world-africa-33049312'))
e2 = ElhancedTree(getQuickTree('http://www.bbc.com/news/business-28978881'))

lxmlTree([e1.tree, prune_first(e1.tree, e2.tree), e2.tree])

for i in range(1000):
    #body = prune_first(e1.tree, e2.tree)
    body = get_first_body(e2.tree, e1.tree)
            
    
print(get_first_body(e2.tree, e1.tree))


viewNode(e1a.tree)

def add_multi_body(args)


    
for x in prune_first(e1.tree, e2.tree).iter(): 
    print(x.tag, x.attrib, x.text)



view_diff(e2.tree, prune_first(e2.tree, e1.tree), url = 'http://www.bbc.com/')


    
view_node(prune_first(e2.tree, e1.tree), url = 'http://www.bbc.com/')



