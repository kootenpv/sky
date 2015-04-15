import re

# def findLeafByText(soup, outcome): 
#     return soup.findAll(text=outcome)

def findLeafByText(tree, outcome):
    return tree.xpath('.//*[text()="{}"]'.format(outcome))

# def findLeafIgnoreWhitespace(soup, outcome): 
#     return soup.findAll(text=re.compile(r"\s*" + outcome.strip() + r"\s*"))

def findLeafIgnoreWhitespace(tree, outcome):
    return tree.xpath('.//*[contains(text(), "{}")]'.format(outcome))

# def findLeafPartial(soup, outcome): 
#     matches = []
#     for x in outcome.split():
#         matches.extend(soup.findAll(text=re.compile(r"\s*" + x.strip() + r"\s*")))
#     return matches

def findLeafPartial(tree, outcome): 
    matches = []
    for x in outcome.split():
        matches.extend(findLeafIgnoreWhitespace(tree, x))
    return matches
    
def findLeaf(tr):
    leafs = []
    leafByText = [findLeafByText(tree, target) for tree, target in zip(tr.trees, tr.targets)]
    if all(leafByText):
        print("findLeafByText...")
        leafs.extend(leafByText)
    leafIgnoreWhitespace = [findLeafIgnoreWhitespace(tree, target) for tree, target in zip(tr.trees, tr.targets)]
    if all(leafIgnoreWhitespace): 
        print("findLeafIgnoreWhite...")
        leafs.extend(leafIgnoreWhitespace) 
    # leafByTopSearch = [findLeafByTopSearch(tree, target, []) for tree, target in zip(tr.trees, tr.targets)]
    # if all(leafByTopSearch):
    #     print("findLeafByTopSearch")
    #     leafs.extend(leafByTopSearch)        
    leafPartial = [findLeafPartial(tree, target) for tree, target in zip(tr.trees, tr.targets)]
    if all(leafPartial): 
        print("findLeafPartial")
        leafs.extend(leafPartial) 
    return leafs

# def findLeafByTopSearch(soupChildren, outcome, sofar, level=0):
#     container = [] 
#     for x in soupChildren: 
#         if hasattr(x, "text"):
#             sofar.append(x) 
#             if re.sub(r"\s+", " ", x.text).strip() == re.sub(r"\s+", " ", outcome).strip():
#                 print("fck yea", level)
#                 return x
#             else:
#                 container.extend([y for y in x.children])
#     if container == []:
#         print("mistake at level", level)
#         return sofar            
#     return findLeafByTopSearch(container, outcome, sofar, level+1)    

# def textGather(soupChildren, sofar=None, level=0):
#     if sofar is None:
#         sofar = []
#     container = [] 
#     for x in soupChildren: 
#         if hasattr(x, "text"):
#             print(level)
#             sofar.append(x.text) 
#             try:
#                 container.extend([y for y in x.children])
#             except:
#                 pass    
#     if not container:
#         print("mistake at level", level)
#         return sofar            
#     return textGather(container, sofar, level+1)
