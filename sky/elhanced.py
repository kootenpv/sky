import lxml.html
import tempfile 
import webbrowser 
import time
from lxmlTree import lxmlTree
from helper import *

class ElhancedTree(): 
    def __init__(self, tree): 
        super().__init__()
        self.leafs = set()
        self.children = set()
        self.tree = tree
        self._reference = list(self.tree.iter())
        self.addDepth(self._reference[0])                        
        
    def addDepth(self, node, depth = 0):
        node.depth = depth
        node.isLeaf = False
        for n in node.iterchildren():
            if bool(list(n.iterchildren())): 
                self.addDepth(n, depth + 1)
            else:
                self.leafs.add(n)    
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

def createNodeDict(t1, t2):
    tkvt1 = {}
    for c in t1.iter():
        if c.attrib: 
            txt = normalize(c.text_content())
            for k,v in c.attrib.items(): 
                tkvt1[(c.tag, k, v, txt)] = c
    return tkvt1            

def prune_first(t1, t2, makeCopy = True):
    if makeCopy:
        from copy import deepcopy
        t1 = deepcopy(t1) 
    tkvt1 = createNodeDict(t1, t2)
    tkvt2 = createNodeDict(t2, t1)
    for c in t2.iter():
        if c.attrib: 
            txt = normalize(c.text_content())
            for k,v in c.attrib.items(): 
                if (c.tag, k, v, txt) in tkvt1: 
                    p = tkvt1[(c.tag, k, v, txt)].getparent()
                    if p is not None:
                        p.remove(tkvt1[(c.tag, k, v, txt)])                            
    return t1

def get_first_body(t1, t2):
    return normalize('\n'.join([x for x in prune_first(t1, t2).itertext() if x.strip()]))

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
