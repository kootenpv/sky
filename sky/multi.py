import numpy as np 

try: 
    from .helper import * 
    from .findTitle import getTitle 
    from .get_date import get_publish_from_meta
    from .findBody import getBody 
    from get_date import get_date_from_content
    from .entities import extract_entities
    from capsule import Capsule
except SystemError: 
    from helper import *
    from findTitle import getTitle 
    from findBody import getBody 
    from get_date import get_publish_from_meta
    from get_date import get_date_from_content
    from entities import extract_entities
    from lxmlTree import lxmlTree
    from capsule import Capsule

c1 = Capsule('http://www.bbc.com/news/world-africa-33049312')
c2 = Capsule('http://www.bbc.com/news/world-asia-china-33044963')


def createNodeDict(t1, t2):
    tkvt1 = {}
    for c in t1.iter():
        if c.attrib: 
            txt = normalize(c.text_content())
            for k,v in c.attrib.items(): 
                key = (c.tag, k, v, txt)
                if key in tkvt1:
                    tkvt1[key].append(c)
                else:    
                    tkvt1[key] = [c]
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
                key = (c.tag, k, v, txt)
                if key in tkvt1: 
                    for case in tkvt1[key]:
                        p = case.getparent()
                        if p is not None:
                            p.remove(case)                            
    return t1

def get_first_body(t1, t2):
    return normalize('\n'.join([x for x in prune_first(t1, t2).itertext() if x.strip()]))

def tree_similarity(t1, t2):
    tkvt1 = createNodeDict(t1, t2)
    tkvt2 = createNodeDict(t2, t1)
    return fscore(tkvt1, tkvt2)


# def createNodeDict(t1, t2):
#     tkvt1 = {}
#     for c in t1.iter():
#         if c.attrib: 
#             txt = normalize(c.text_content())
#             for k,v in c.attrib.items(): 
#                 tkvt1[(c.tag, k, v)] = c
#     return tkvt1    

import justext    

for x in justext.justext(c1.html, justext.get_stoplist('English')):
    if not x.is_boilerplate:
        print(x.text)


for x in c1.tree.iter():
    print(x.tag, get_text_and_tail(x))
    print('//////////////////////////////////////////////////////////')


t = prune_first(c1.tree, c2.tree)

for x in t.xpath('//a'):
    x.getparent().remove(x)

stupid = True
while stupid:
    stupid = False 
    for x in t.iter():
        try:
            if not normalize(x.text_content()):
                stupid = True
                x.getparent().remove(x)
        except: 
            pass

view_tree(t)

county = Counter([(str(x.tag), str(x.attrib)) for x in t.iter()])
for x in county:
    print(x, county[x])
    

county = Counter([(str(x.tag), str(x.attrib)) for x in c2.tree.iter()])
for x in county:
    print(x, county[x])    








c1 = Capsule('http://www.lazygamer.net/e3-2015/bethesda-reveals-hearthstone-competitor-elder-scrolls-legend/')
c2 = Capsule('http://www.lazygamer.net/playstation-4-2/call-of-duty-switches-allegiances-from-xbox-to-playstation/')




c1 = Capsule('http://www.infoworld.com/article/2935436/machine-learning/ibm-spark-bluemix-machine-learning.html')
c2 = Capsule('http://www.infoworld.com/article/2897287/big-data/5-reasons-to-turn-to-spark-for-big-data-analytics.html')

c1 = Capsule('http://bankinnovation.net/2014/01/housing-continues-to-rebound/')
c2 = Capsule('http://bankinnovation.net/2015/06/ally-leverages-analytics-for-smarter-mobile-banking/')


