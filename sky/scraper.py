from training import *
from findLeaf import *
import re
from lxml.html import fromstring
from lxml.html import tostring

def stripReasonableWhite(x):
    return re.sub(r"\s+", " ", x).strip()
    
def splitN(txt, outcome):
    # consider splitting to get result
    txt = stripReasonableWhite(txt)
    outcome = stripReasonableWhite(outcome)
    splitables = set(txt.replace(outcome, '', 1)) - set(' ') 
    options = set()
    for s in splitables:
        for i, x in enumerate(txt.split(s)):
            if stripReasonableWhite(x) == stripReasonableWhite(outcome):
                options.add((s, i))
    return options            

def splitSolution(how):
    def solution(txt):
        return txt.split(how[0])[how[1]]
    return solution    
    
def asNumeric(x): 
    return re.sub("[^0-9]", "", x)

def applySolutionChain(solution, x): 
    for sol in solution: 
        if isinstance(sol, dict):
            x = x.find(**sol)
        else:    
            x = sol(x)
    return x    

def buildSolution(training):
    res = findLeaf(training)
    print("len(res)", len(res))
    x = findSharedKeyValues(training, res)
    print("len(shared)", len(x))
    solutions = secondLevelDown(training.soups[0], training.targets[0], x)
    print("len(solutions)", len(solutions))
    return solutions

def tryUniqueID(c, sp):
    return len(sp.findAll(c.name, attrs=c.attrs)) == 1

def buildNewSolution(tr):
    childs = []
    num = 0
    options = []
    for soup, target in zip(tr.soups, tr.targets):
        print('num',num)
        num+=1
        for c in soup.findChildren():
            try:
                if c.name not in ['body', 'html']:
                    if target in c.text:
                        childs.append([c,  len(c.text)])
            except:
                pass        

        tmp = []            
        for i,x in enumerate(childs[::-1]): 
            if tryUniqueID(x[0], soup):
                attrs = x[0].attrs
                attrs['name'] = x[0].name
                attrs = {'attrs' : attrs}
                if x[0].text == target:
                    tmp.append((attrs, BeautifulSoup.get_text))
                elif stripReasonableWhite(x[0].text) == stripReasonableWhite(target):     
                    tmp.append((attrs, BeautifulSoup.get_text, stripReasonableWhite))
                elif splitN(x[0].text, target):    
                    for splitable in splitN(x[0].text, target):
                        tmp.append((attrs, BeautifulSoup.get_text, splitSolution(splitable)))
                else: 
                    print(len([y for y in x[0].children]))
            else:
                print('not unique', len([y for y in x[0].children])) 
        options.append(tmp)
    good_options = [] 
    if options: 
        for x in options[0]:
            if all(x in y for y in options[1:]): 
                good_options.append(x)
    return good_options    
    
#testAutoScraperSolutions(buildSolution(tr), tr, False)

    

tr1 = Training("marktplaats-testcase1", "/Users/pascal/GDrive/sky_package/sky/tests/").load()
# tr2 = Training("nieuwsdumper-testcase1", "/Users/pascal/GDrive/sky_package/sky/tests/").load()
tr3 = Training("nieuwsdumper-testcase2", "/Users/pascal/GDrive/sky_package/sky/tests/").load()
# tr4 = Training("bouwmaterieel-testcase1", "/Users/pascal/GDrive/sky_package/sky/tests/").load()
# tr5 = Training('betterdoctor-doctor-referalls', '/Users/pascal/GDrive/sky_package/sky/tests/').load()
tr6 = Training("pypi-author", "/Users/pascal/GDrive/sky_package/sky/tests/").load()

# Moet wel text_content zijn, anders ga je dingen mislopen!!!!!!!!!!!!!
# plottwist misschien gewoon 2 methoden

def getMatchedNodes(tr):
    matchedLeafs = []
    for tree, outcome in zip(tr.trees, tr.targets):
        matchedLeaf = {'text' : [], 'tail' : [], 'attrib' : [], 'content' : []}
        for x in tree.iter():
            if x.text and outcome in x.text:
                matchedLeaf['text'].append(x)
            if x.tail and outcome in x.tail:
                matchedLeaf['tail'].append(x)    
            if x.attrib and any([outcome in y for y in x.attrib.values()]):
                matchedLeaf['attrib'].append(x)
        matchedLeafs.append(matchedLeaf)
    return matchedLeafs


def getMatchedTextContentNodes(tree, outcome, container): 
    children = tree.getchildren()
    if children:
        for c in children:
            if outcome in c.text_content():
                container.append(c)
                getMatchedTextContentNodes(c, outcome, container)
    return container            

for i in range(1000):
    res = getMatchedNodes(tr3)
    for tree, outcome, r in zip(tr3.trees, tr3.targets, res): 
        r['content'] = getMatchedTextContentNodes(tree, outcome, []) 
        
div = fromstring('<div>I have <strong>5</strong> friends</div>')
