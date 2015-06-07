try:
    from .helper import getQuickTree
    from .findTitle import getTitle, getTitle2
    from .training import Training
except SystemError:
    from helper import getQuickTree
    from findTitle import getTitle, getTitle2
    from training import Training

DOMAIN = 'http://theneeds.com'

ps = ["/news", "/shop", "/social", "/read", "/music", "/travel", "/video", "/sport", "/food", "/money", "/game", "/learn", "/work"]


# seen = set()
# titles = []
# links = []
# for p in ps:
#     tree = getQuickTree(DOMAIN + p)
#     for card in tree.xpath('//div[contains(@class, "view view-card")]'):
#         sources = card.xpath('.//div[@class="view-card-source"]')
#         titties = card.xpath('.//div[@class="view-card-title"]/a')
#         descs = card.xpath('.//div[@class="view-card-descr"]')
#         for s,t,d in zip(sources, titties, descs):
#             stext = s.text_content().strip()
#             link = t.get('data-href-ext')
#             if stext not in seen: 
#                 if link is not None:
#                     seen.add(stext)
#                     titles.append(t.text_content())
#                     links.append(link)

# assert '\n' not in 'asdf'.join(titles)
# assert '\t' not in 'asdf'.join(titles)

# with open('theneeds.tsv', 'w') as f:
#     f.write('\n'.join(['{}\t{}'.format(l, t.replace('\n', ' ')) for l, t in zip(links,titles)]))

with open('theneeds.tsv') as f: 
    links = [x.split('\t')[0] for x in f.read().split('\n')]

# tr = Training('titles', '/Users/pascal/GDrive/virtual-python/sky/sky/theneeds-test/').load()
# tr.addLinks(links[20:], False, len(tr.targets))
# tr.classify()
# tr.save()

tr = Training('titles', '/Users/pascal/GDrive/virtual-python/sky/sky/theneeds-test/').load()

total1 = 0
for i,(x,y,l) in enumerate(zip(tr.trees, tr.targets, tr.links)):
    try:
        res = getTitle(x)
        if res != y:
            print(i, l, ':::::', res, '|||||', y) 
        else:
            total1+=1    
    except:
        print(False) 
    print(total1)    

        
def add_depth(node, depth = 1):
    global maxd
    for n in node.iterchildren(): 
        if n.text:
            if len(n.text) > 200:
                print(n.text)
        else:
            print(0)    
        if depth > maxd[1]:
            maxd = [n, depth]
        add_depth(n, depth + 1)

maxd = [None, 0]
add_depth(tr.trees[0].xpath('/html')[0], 1)

d = {}
for node in root:
    key = node.tag
    if node.getchildren():
        for child in node:
            key += '_' + child.tag
            d.update({key: child.text})
    else:
        d.update{key: node.text}


for tree in tr.trees:
    maxl = [None, None, 0]
    for x in tree.iter():
        tc = x.text if x.text else ''
        tl = x.tail if x.tail else '' 
        if '{' in tc+tl:
            continue
        l = len(tc+tl)
        if l > maxl[2]:
            maxl = [x, tc+tl, l]
    print(maxl[1])            

for tree in tr.trees:    
    d = {}
    for node in tree.xpath('//body')[0]:
        if node.getchildren():
            tcp = node.text_content() 
            if tcp:
                ltcp = len(tcp)
                for child in node: 
                    tcc = child.text_content()
                    if tcc: 
                        d[node] = max(d[node], ltcp / len(tcc)) if (node in d) else ltcp / len(tcc)
    if d:                    
        big_change = max(d, key = d.get) 
        print(big_change.text_content())


def getTKV(tree):
    tkv = set()
    for c in tree.iter():
        if c.attrib: 
            for k,v in c.attrib.items():    
                tkv.add((c.tag, k, v, c))
    return tkv        


    
t1= getQuickTree('http://www.nieuwsdumper.nl/nieuws/1454/eerste-volvo-fmx-410-8x4-tridem-betonmixer-voor-bck.html')
t2 = getQuickTree('http://www.nieuwsdumper.nl/nieuws/1656/terex-en-ihi-voor-f-v-s-loonwerk-incl-video-.html')    


tkv1 = getTKV(t1)
tkv2 = getTKV(t2)

children = {}
parents = {}

import re

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

    return t1
                        
viewString(lxml.html.tostring(tt).decode('utf8'), webdriver.Firefox())

                


a = """

asdfasdf

asdfasdf

"""
