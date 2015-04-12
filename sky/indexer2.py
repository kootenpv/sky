import numpy as np
import os
import justext
from bs4 import BeautifulSoup
import re
import codecs
import lxml
import sys

if True:
    try:
        from urllib import urlopen
    except: 
        from urllib.request import urlopen

sys.path.append('/Users/pascal/Dropbox/watsonTestSuite/')
from htmlTree import *

collectionName = 'OneMediq'
PATH = '/Users/pascal/Dropbox/watsonTestSuite/collections/' + collectionName + '/'
OUT_PATH = '/Users/pascal/Dropbox/watsonTestSuite/collections/' + collectionName + '-snippets/'

if not os.path.exists(OUT_PATH):
    os.makedirs(OUT_PATH)

class CrawledDocs():    
    def __init__(self, inp, maxN=10000000):                
        if isinstance(inp, str):
            if os.path.isdir(inp):
                self.readfiles(inp, maxN)
            else:
                self.readweb(inp)
        else: 
            self.readweb(inp)
    def readfiles(self, PATH, maxN):
        soups = []
        htmls = []
        lxmls = []
        file_names = []
        num = 0
        for root, dirs, files in os.walk(PATH): 
            for name in files:
                if num >= maxN:
                        break
                if ("DS" not in name) and ('links.txt' not in name): 
                    num += 1
                    with open(root + "/" + name, encoding='latin-1') as page:
                        html = page.read()
                        soup = BeautifulSoup(html).html
                        htmls.append(html)
                        lxmls.append(lxml.html.fromstring(html))
                        soups.append(soup) 
                        file_names.append(name)
        self.soups = soups
        self.lxmls = lxmls
        self.htmls = htmls
        self.file_names = file_names
    def readweb(self, inp):
        if isinstance(inp, str):
            htmls = [urlopen(inp).read()]
            self.file_names = [inp]
        elif isinstance(inp, list):
            self.htmls = [urlopen(url).read() for url in inp]
            self.lxmls = [lxml.html.fromstring(x) for x in self.htmls]
            self.soups = [BeautifulSoup(x) for x in self.htmls]
            self.file_names = inp        

class IndexImportant():
    def __init__(self, crawledDocs):
        self.cD = crawledDocs
        
    def textGather(self, soupChildren, sofar=None, level=0):
        if sofar is None:
            sofar = []
        container = [] 
        for x in soupChildren: 
            if hasattr(x, "text"):
                sofar.append([x, x.text]) 
                try:
                    container.extend([y for y in x.children])
                except:
                    pass    
        if container == []:
            return(sofar)            
        return(self.textGather(container, sofar, level+1))        

    def textGatherLXML(self, soupChildren, sofar=None, level=0):
        if sofar is None:
            sofar = []
        container = [] 
        for x in soupChildren: 
            try:
                children = x.getchildren()
            except:
                children = []
            if children: 
                container.extend([y for y in children])
            try:
                sofar.append([x, x.text_content()])
            except:
                sofar.append([x, '']) 
        if container == []:
            return(sofar) 
        return(self.textGatherLXML(container, sofar, level+1))

    def filterUniques(self, seq):
        seen = set()
        seen_add = seen.add
        seq = [(x[0], re.sub("\s+", " ", x[1]).strip()) for x in seq]
        return([ x for x in seq if not (x[1] in seen or seen_add(x[1]))])

    def trainer(self, trees, n_max = 20):
       ress = [] 
       if 'bs4' in trees[0].__module__:
           for tree in trees[:n_max]: 
               ress.append(self.filterUniques(self.textGather(tree))) 
       else:
           for tree in trees[:n_max]: 
               ress.append(self.filterUniques(self.textGatherLXML(tree)))     
       trained = [] 
       for x in ress[0]: 
           if all([x[1] in [z[1] for z in y] for y in ress[1:]]): 
               trained.append(x[1]) 
       return(trained)

    def tester(self, tree, trained):
        result = []
        if 'bs4' in tree.__module__ :
            unis = self.filterUniques(self.textGather(tree))
        else:
            unis = self.filterUniques(self.textGatherLXML(tree))
        for x in unis:        
            if x[1] not in trained:
                result.append(x)
        return(result)        

    def removeJavascript(self, ts):
        result = []
        java_script_blacklist = ['\$([^)]+).', 'var [^ ]+ [^;]+;']
        for x in ts:
            if 'document' not in x[1]:
                if "();" not in x[1]: 
                    if all([not re.search(y, x[1]) for y in java_script_blacklist]):
                        result.append(x)
        return(result)            

    def pruner(self, ts, pruning, remove_javascript=True, printText=True): 
        # remove javascript
        if remove_javascript:
            ts = self.removeJavascript(ts)
        # prune 
        if pruning:
            leftover = []
            done = []            
            for x in ts:
                notinit = True 
                for y in ts:
                    if (x[1] in y[1]) & (y[1] != x[1]):
                        notinit = False
                        break
                if notinit:
                    leftover.append(x)
            ts = leftover        
        if printText: 
            if 'bs4' in ts[0][0].__module__:
                return([x[0].text for x in ts])
            else:
                return([x[0].text_content() for x in ts])
        return(ts)            

    def prepare(self, trees, pruning=True, remove_javascript=True, printText=True, train_n_max = 20): 
        tr = self.trainer(trees, train_n_max)
        results = []
        for tree in trees:
            ts = self.tester(tree, tr)
            results.append(self.pruner(ts, pruning, remove_javascript, printText))
        self.results = results

    def write_results(self, OUT_PATH):
        for x, y in zip(self.results, self.cD.file_names):
            with codecs.open(OUT_PATH + y + ".txt", 'w', 'utf-8-sig') as f:
                f.write("\n\n\n".join(x)) 

    def getsubidx(self, list1, list2):
        l1, l2 = len(list1), len(list2)
        for i in range(l1-l2):
            if list1[i:i+l2] == list2:
                return(i)                
                
    def pinpoint(self, lxmls, which):
        #res = self.prepare(lxmls[:20], True, printText=False)
        res = self.results
        whole = lxmlTree(lxmls[which], True, False) 
        abc = 'abcdefghijklmnopqrstuvwxyz' * 100
        for num, annot in enumerate(res[which]):
            wholeE = ['+' + ''.join(x.strip().split('+')[1:]) for x in whole.split('\n') if x.strip()]     
            part = lxmlTree(annot[0], True, False) 
            partE = ['+' + ''.join(x.strip().split('+')[1:]) for x in part.split('\n')[1:] if x.strip()]
            ind = max(2, self.getsubidx(wholeE, partE) - 2)
            tmp = whole.split('\n')
            match_len = len(partE)
            for i in range(len(tmp)):
                if i > ind and i < ind + match_len + 2:
                    tmp[i] += '  -(' + str(abc[num]) + ')-'
            whole = "\n".join(tmp) 
        print(whole)

cD = CrawledDocs(PATH, 100)

a = IndexImportant(cD)

a.prepare(cD.lxmls, True, printText=False)
a.pinpoint(cD.lxmls, 1)

a.prepare(cD.lxmls, True, printText=True)

#a.write_results(OUT_PATH)

# res = self.prepare(lxmls[:20], True, printText=False)

cD.htmls = [x for i,x in enumerate(cD.htmls) if i in ok]
cD.lxmls = [x for i,x in enumerate(cD.lxmls) if i in ok]
cD.file_names = [x for i,x in enumerate(cD.file_names) if i in ok]

#pinpoint(cD.lxmls, 0)

# a = IndexImportant(cD)

# a.prepare(a.cD.lxmls, printText=False)

# a.write_results(OUT_PATH)

# pinpoint(a.cD.lxmls, 0)

# def get_xpath(res):
#     things = []
#     for x in res:
#         things.append([(y[0].name, y[0].attrs) for y in x])
#     uniques = []
#     for x in things[0]:
#         if all([x in y for y in things]):
#             uniques.append(x)
#         for y in things:
#             if x not in y:
#                 print y
#     return uniques

# def get_xpaths(soups):
#     res = prepare(soups, True, printText=False)
#     xpaths = get_xpath(res)

#     allnths = []
#     for i in range(len(soups)):
#         nths = []
#         for xpath, r in zip(xpaths, res[i]):
#             for num, y in enumerate(soups[i].findAll(xpath)):
#                 if y == r[0]:
#                     nths.append(num)
#         allnths.append(nths)            

#     return allnths    
#     verified = []    
#     for num, i in enumerate(allnths[0]):
#         if all([x[num] == i for x in allnths]):
#             verified.append(num)

#     verified_xpaths = [x for num,x in enumerate(xpaths) if num in verified]
#     nths = [x for num,x in enumerate(allnths[0]) if num in verified]

#     print len(xpaths), len(nths)
#     print verified_xpaths, nths
#     return [soups[0].findAll(x)[y] for x,y in zip(verified_xpaths, nths)]

# test = get_xpaths(soups)

# pinpoint(lxmls, 0)

# lxmlTree(lxmls[0], namedAttrs=[])

# lxmlTree(res[0][1][0])



def textGather(soupChildren, sofar=None, level=0):
    if sofar is None:
        sofar = []
    container = [] 
    for x in soupChildren: 
        if hasattr(x, "text"):
            sofar.append([x, x.text, level]) 
            try:
                container.extend([y for y in x.children])
            except:
                pass    
    if container == []:
        return(sofar)            
    return(textGather(container, sofar, level+1))        


urls = ['http://www.nieuwsdumper.nl/nieuws', 'http://www.nieuwsdumper.nl/faq', 'http://www.nieuwsdumper.nl/contact',
        'http://www.nieuwsdumper.nl/nieuws/1599/doosan-dl420-3-voor-de-rivierendriesprong-papendrecht-bv.html',
        'http://www.nieuwsdumper.nl/nieuws/1596/takeuchi-cabrio-voor-van-der-kooij-maasland.html',
        'http://www.nieuwsdumper.nl/nieuws/1588/de-vries-neemt-terex-tc35-in-gebruik.html']

htmls = [urllib.request.urlopen(url) for url in urls]

soups = [BeautifulSoup(html) for html in htmls]


def taglevels(soup):
    return [(x[0].name, x[2]) for x in textGather(soup)]

def matchpercent(soup1, soup2, method):
    counted_items = {}
    for item in method(soup1):
        counted_items[item] = counted_items.get(item, 0) + 1

    counted_items2 = {}
    for item in method(soup2):
        counted_items2[item] = counted_items2.get(item, 0) + 1    

    total = sum(counted_items.values()) + sum(counted_items2.values())
    matched = 0    
    for x in counted_items:
        if x in counted_items2:
            matched += counted_items[x] 
    for x in counted_items2:
        if x in counted_items2:
            matched += counted_items2[x]
    return matched, total, matched/total
    
def keyattr_levels(soup):
    combined = []
    for x in textGather(soup):
        for y in x[0].attrs:
            combined.append((y, x[2]))
    return combined

def attr_levels(soup):
    combined = []
    for x in textGather(soup):
        for y in x[0].attrs:
            combined.append((y, x[0].attrs[y], x[2]))
    return combined
    
attr_levels(soups[0])


res = []
for x in soups:
    tmp = []
    for y in soups:
        tmp.append(round(matchpercent(x,y,keyattr_levels)[2],3))
    res.append(tmp)    

res = np.array(res)    
        

res2 = []
for x in soups:
    tmp = []
    for y in soups:
        tmp.append(round(matchpercent(x,y,taglevels)[2],3))
    res2.append(tmp)    


res3 = []
for x in soups:
    tmp = []
    for y in soups:
        tmp.append(round(matchpercent(x,y,attr_levels)[2],3))
    res3.append(tmp)    

    
res3 = np.array(res3)

np.round(hmean((res,res2,res3)),2)

filenames = []
for root, dirs, files in os.walk('/Users/pascal/bert-google-places-cache/webpage/', topdown=False):
    for name in files:
        filenames.append(os.path.join(root, name))

filenames = [x for x in filenames if '.nl' in x]


from sklearn.cluster import SpectralClustering as sc

sc(3,affinity='precomputed').fit_predict(hmean((res,res2,res3)))

