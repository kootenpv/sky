import re

def findLeafByText(soup, outcome): 
    return soup.findAll(text=outcome)

def findLeafIgnoreWhitespace(soup, outcome): 
    return soup.findAll(text=re.compile(r"\s*" + outcome.strip() + r"\s*"))

def findLeafPartial(soup, outcome): 
    matches = []
    for x in outcome.split():
        matches.extend(soup.findAll(text=re.compile(r"\s*" + x.strip() + r"\s*")))
    return matches

def findLeaf(tr):
    leafs = []
    leafByText = [findLeafByText(soup, target) for soup, target in zip(tr.soups, tr.targets)]
    if all(leafByText):
        print("findLeafByText...")
        leafs.extend(leafByText)
    leafIgnoreWhitespace = [findLeafIgnoreWhitespace(soup, target) for soup, target in zip(tr.soups, tr.targets)]
    if all(leafIgnoreWhitespace): 
        print("findLeafIgnoreWhite...")
        leafs.extend(leafIgnoreWhitespace) 
    leafByTopSearch = [findLeafByTopSearch(soup, target, []) 
                           for soup, target in zip(tr.soups, tr.targets)]
    if all(leafByTopSearch):
        print("findLeafByTopSearch")
        leafs.extend(leafByTopSearch) 
    leafPartial = [findLeafPartial(soup, target) for soup, target in zip(tr.soups, tr.targets)]
    if all(leafPartial): 
        print("findLeafPartial")
        leafs.extend(leafPartial) 
    return leafs

def findLeafByTopSearch(soupChildren, outcome, sofar, level=0):
    container = [] 
    for x in soupChildren: 
        if hasattr(x, "text"):
            sofar.append(x) 
            if re.sub(r"\s+", " ", x.text).strip() == re.sub(r"\s+", " ", outcome).strip():
                print("fck yea", level)
                return x
            else:
                container.extend([y for y in x.children])
    if container == []:
        print("mistake at level", level)
        return sofar            
    return findLeafByTopSearch(container, outcome, sofar, level+1)    

def textGather(soupChildren, sofar=None, level=0):
    if sofar is None:
        sofar = []
    container = [] 
    for x in soupChildren: 
        if hasattr(x, "text"):
            print(level)
            sofar.append(x.text) 
            try:
                container.extend([y for y in x.children])
            except:
                pass    
    if not container:
        print("mistake at level", level)
        return sofar            
    return textGather(container, sofar, level+1)        

def filterUniques(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]
    
def tester(soups):
    ress = []
    for soup in soups:
        ress.append(filterUniques([re.sub(r"\s+", " ", x) for x in textGather(soup) if x]))
    new = []
    for x in ress[0]:        
        if any([bool(x not in y) for y in ress[1:]]): 
            new.append(x)
    done = []                
    for x in new:
        if x not in done: 
            try:
                print(x)
                done.append(x)
            except:
                pass
    return done        


