# import re
import os
import json

resources = {}
# Explanation: http://wiki.dbpedia.org/Downloads2015-04
# Link to this set: http://downloads.dbpedia.org/2015-04/core-i18n/en/instance-types_en.nt.bz2
with open('/Users/pascal/Downloads/instance_types_en.nt') as f: 
    for line in f:
        try:
            parts = line.split()
            first_part = parts[0]
            if first_part.count('/') == 4:
                name = first_part.split('/')[-1].replace('_', ' ').lower()[:-1]
                if len(name.split()) > 3:
                    continue
                pos = name.find('  ')
                if pos > -1:
                    name = name[:pos]       
                if 'ontologydesignpatterns' in parts[2]:                    
                    continue
                if 'w3.org' in parts[2]:                    
                    continue
                if name not in resources: 
                    resources[name] = set() 
                resources[name].add(parts[2].split('/')[-1][:-1]) 
        except IndexError:
            pass    

# resources start with 'http://dbpedia.org/resource/'

# types = set()
# for name in resources:
#     m = re.search(r'(\(.+\))', name)
#     if m:
#         types.add(m.groups()[0].lower())            

stripped_resources = {}
for x in resources:
    if any([y in x for y in '0123456789']): 
        if '%' not in x: 
            continue
    pos = x.find('(') 
    if pos > -1:
        stripped_resources[x[:pos].strip()] = list(resources[x])
    else:    
        stripped_resources[x.strip()] = list(resources[x])

#######################################################################################################################        

fname = os.path.join(os.path.dirname(__file__), 'dbpedia.json')
with open(fname, 'w') as f: 
    json.dump(stripped_resources, f)

# from ZODB.FileStorage import FileStorage
# from ZODB.DB import DB

# import transaction
# from BTrees.OOBTree import OOBTree
        
# storage = FileStorage('/Users/pascal/GDrive/appear/Data.fs')
# db = DB(storage)
# connection = db.open()
# root = connection.root()

# root['dbpedia'] = OOBTree(stripped_resources)
# transaction.commit()
