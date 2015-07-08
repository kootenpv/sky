import numpy as np 
import lxml.html
from collections import Counter

try: 
    from .helper import * 
    from .findTitle import getTitle 
    from .findBody import getBody 
    from .get_date import get_dates
    from .entities import extract_entities
except SystemError: 
    from helper import *
    from findTitle import getTitle 
    from findBody import getBody 
    from get_date import get_dates
    from entities import extract_entities
    from lxmlTree import lxmlTree
    from capsule import Capsule

def createNodeDict(t1):
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

def create_tree_recursively(node, node_dict, parent):
    for child in node.getchildren():
        parent.append(copy.deepcopy(child))
        create_tree_recursively(child)
    return parent    

# create_tree_recursively(c.tree, node_dict, )                     
    
def prune_first(t1, t2):
    tkvt1 = createNodeDict(t1)
    for c in t2.iter():
        if c.attrib: 
            txt = normalize(c.text_content())
            for k,v in c.attrib.items(): 
                key = (c.tag, k, v, txt)
                if key in tkvt1: 
                    for case in tkvt1[key]:
                        try:
                            case.drop_tree()
                            break
                        except:
                            pass
    return t1


def get_multi_body(tr1):
    return normalize('\n'.join([x for x in tr1.itertext() if x.strip()]))

def tree_similarity(t1, t2):
    tkvt1 = createNodeDict(t1)
    tkvt2 = createNodeDict(t2)
    return fscore(tkvt1, tkvt2)

def choose_most_similar(t1, trees_urls):
    tree_similarities = [(tree_url[0], tree_url[1], tree_similarity(t1, tree_url[0])) for tree_url in trees_urls]
    if tree_similarity:
        return sorted(tree_similarities, key = lambda x: x[2], reverse = True)[0]
    return False


    
# def createNodeDict(t1, t2):
#     tkvt1 = {}
#     for c in t1.iter():
#         if c.attrib: 
#             txt = normalize(c.text_content())
#             for k,v in c.attrib.items(): 
#                 tkvt1[(c.tag, k, v)] = c
#     return tkvt1    

if False:
    # c1 = Capsule('http://www.bbc.com/news/world-africa-33049312')
    # c2 = Capsule('http://www.bbc.com/news/world-asia-china-33044963')

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







# def attrib_key_contains(node, tag = '', attr_allow = '', sought_value = ''):
#     if tag not in node.tag:
#         return False
#     for a in node.attrib:
#         if attr_allow in a:
#             if sought_value in node.attrib[a]:
#                 return node.tag, a, node.attrib[a]
#     return False        

# def extract_from_node_by_text_content(node):
#     return normalize(node.text_content())

# def extract_from_node_by_attribute(node, key):
#     return node.attrib.get(key, '')
    
# def generate_rule_dictionary():
#     headers = ['h{}'.format(i) for i in range(1, 5)]
#     tags = ['strong', 'b', 'div']
#     atts = ['id', 'class', '']
#     res = {k : {kk : {} for kk in atts} for k in headers + tags} 
#     it = 0
#     for h in headers:
#         for k in atts:
#             it += 1
#             res[h][k]['title'] = it 
#             it += 1
#             res[h][k][''] = it
#             it += 1    
#         res[h]['']['title'] = it
#         it += 1    
#         res[h][''][''] = it

#     # for t in tags:
#     #     for k in atts:
#     #         it += 1
#     #         res[t][k]['title'] = it 
#     #         it += 1
#     #         res[t][k][''] = 100 
#     #         it += 1
#     #     res[t]['']['title'] = it    
#     #     it += 1
#     #     if t != 'div':
#     #         res[t][''][''] = it    

#     return res

# def get_score_from_title_dict(node, dc):
#     tag_found = dc.get(node.tag, '')
#     if tag_found:
#         maxi = 100
#         for attribute in node.attrib:
#             key_found = dc[node.tag].get(attribute, '')
#             if key_found:
#                 if 'title' in node.attrib[attribute]: 
#                     maxi = min(maxi, dc[node.tag][attribute]['title'])
#                 else:    
#                     maxi = min(maxi, dc[node.tag][attribute][''])
#         #if maxi == 100:
#             #maxi = dc[node.tag][''][''] 
#         return maxi, node.text_content()
#     else:    
#         return 101, ''
            

# def get_meta_titles(tree): 
#     res = []
#     head = tree.find('head')
#     if head is not None:
#         for xp in ['.//title/text()', './/meta[contains(@name, "title")]/@content', 
#                    './/meta[contains(@property, "title")]/@content']:
#             res.extend(head.xpath(xp))
#     return res    
        
    


# def sorted_title_candidates(tree, rule_dc):
#     mins = []            
#     for node in tree.iter():
#         score, ele = get_score_from_title_dict(node, rule_dc)
#         stripped_ele = ele.strip()
#         if stripped_ele and score != 101 and len(ele.split()) < 5:
#             mins.append((score, stripped_ele))

#     return [x[1] for x in sorted(mins)]


# tr = getQuickTree('http://www.bbc.com/news/world-africa-33049312')

# tr1 = getQuickTree('http://www.bbc.com/news/science-environment-33268180')

# tr2 = getQuickTree('http://www.nieuwsdumper.nl/nieuws/1454/eerste-volvo-fmx-410-8x4-tridem-betonmixer-voor-bck.html')

# tr3 = getQuickTree('http://www.nieuwsdumper.nl/nieuws/1671/eerste-doosan-vijf-serie-in-friesland-afgeleverd-aan-kor-de-boer.html')

# rule_dict = generate_rule_dictionary()

# sorted_title_candidates(tr2, rule_dict, val_dict)

# xpaths = ['//title', '//*[contains(@name, "title")]', '//h1[contains(@id, "title")]', '//h1[contains(@class, "title")]', '//h1[@*="title"]', '//*[contains(@id, "title")]',  '//meta[contains(@property, "title")]', '//meta[contains(@property, "title")]/@content', '//h1', '//h2', '//*[contains(@class, "title")]', '//*[@title]', '//h3', '//h4', '//strong', '//*[contains(@*, "headline")]', '//*[contains(@*, "Headline")]']

# for i in range(10000):
#     for xp in xpaths:
#         xresults = t.xpath(xp)



# def get_title_from_text_meta(tree):
#     texts = sorted_title_candidates(tree, rule_dict)
#     metas = get_meta_titles(tree)
#     maxs = 0
#     ele = ''
#     for x in texts:
#         xs = x.lower().split()
#         for y in metas:            
#             ys = y.lower().split()
#             newm = fscore(xs, ys)
#             if newm > maxs:
#                 maxs = newm
#                 ele = x
#     return ele


# for i in range(1000):
#     get_title_from_text_meta(tr)

# def createNodeSet(t1, t2):
#     tkvt1 = set()
#     for c in t1.iter():
#         if c.attrib: 
#             txt = normalize(c.text_content())
#             if txt: 
#                 for k,v in c.attrib.items(): 
#                     key = (c.tag, k, v, txt)
#                     tkvt1.add(key)
#     return tkvt1            
    
# def rule_exclude_dict(t1, t2, makeCopy = True):
#     tkvt1 = createNodeSet(t1, t2)
#     ecdict = {}
#     for c in t2.iter():
#         if c.attrib: 
#             txt = normalize(c.text_content())
#             if txt:
#                 for k,v in c.attrib.items(): 
#                     key = (c.tag, k, v, txt)
#                     if key in tkvt1: 
#                         if key[0] not in ecdict:
#                             ecdict[key[0]] = {}
#                         if key[1] not in ecdict[key[0]]:
#                             ecdict[key[0]][key[1]] = {}
#                         if key[2] not in ecdict[key[0]][key[1]]:
#                             ecdict[key[0]][key[1]][key[2]] = []
#                         ecdict[key[0]][key[1]][key[2]].append(key[3]) 
#     return ecdict

# exdict = rule_exclude_dict(tr2, tr3)


# for c in tr3.iter():
#     t = c.tag
#     if c.attrib: 
#         for k,v in c.attrib.items(): 
#             if t in exdict and k in exdict[t] and v in exdict[t][k]: 
#                 break
#         else:
#             continue
#         txt = normalize(c.text_content())
#         if txt and txt in exdict[t][k][v]:
#             continue
#     print(get_text_and_tail(c))


# dc = set()    
# dc2 = set()
# for c in tr2.iter():
#     dc.add(c.text_content())

# for c in tr3.iter():
#     dc2.add(c.text_content())

# ts = dc2 - dc

# bla = set()
# for x in ts: 
#     if not any(y in x and x != y for y in ts):
#         bla.add(x)






    
