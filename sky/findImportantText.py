try:
    from .helper import *
    from .findTitle import getTitle, getTitle2
    from .training import Training
except SystemError:
    from helper import *
    from findTitle import getTitle, getTitle2
    from training import Training

tr = Training("nieuwsdumper-testcase1", "/Users/pascal/GDrive/virtual-python/sky/sky/tests/").load()
tr2 = Training("nieuwsdumper-testcase1", "/Users/pascal/GDrive/virtual-python/sky/sky/tests/").load()

def prune_first(t1, t2):
    tkvt1 = {}
    for c in t1.iter():
        if c.attrib: 
            txt = normalize(c.text_content())
            for k,v in c.attrib.items(): 
                tkvt1[(c.tag, k, v, txt)] = [c.getparent(), c]

    tkvt2 = {}
    for c in t2.iter():
        if c.attrib: 
            txt = normalize(c.text_content())
            for k,v in c.attrib.items(): 
                tkvt2[(c.tag, k, v, txt)] = [c.getparent(), c]


    for c in t2.iter():
        if c.attrib: 
            txt = normalize(c.text_content())
            for k,v in c.attrib.items(): 
                if (c.tag, k, v, txt) in tkvt1: 
                    try:
                        tkvt1[(c.tag, k, v, txt)][0].remove(tkvt1[(c.tag, k, v, txt)][1])
                    except:
                        print((c.tag, k, v, txt))

prune_first(tr.trees[0], tr.trees[1])    


