DATE_TARGET = '2015-01-01'
WORD_TARGET = 'Goed'
INT_TARGET = '1'
FLOAT_TARGET = '1.0'
NUMBER_TARGET = '1,000'

import sys
sys.path.append("/Users/pascal/GDrive/sky_package/sky/")
from utils import *
from training import *
from findLeaf import *
from scraper import *


# attributed
# - uniquely
# - not-uniquely

# elemented
# - uniquely
# - not-uniquely

# floating-element
# - uniquely
# - not-uniquely
>
def elem(tag = '', attrs = '', inner_text = ''):
    if not attrs and not inner_text:
        return tag
    if attrs != '':
        attrs = ' ' + attrs
    return '<{}{}>{}</{}>'.format(tag, attrs, inner_text, tag)

ele = elem('div', '', elem('a', 'href="/"', 'bla'))
    
for i in range(100000):
    sp = BeautifulSoup(ele)

tr.targets = ['bla1', 'bla2']
elems = [elem('div', 'class="test"',
              elem('div', '', 
                   elem('a', 'href="/"') + target)) 
         for target in tr.targets]
tr.soups = [BeautifulSoup(ele + 'PreventBodyAndHTML') for ele in elems]

buildSolution(tr)
    

def confuscate(ele, what):
    if what == 'attr':
        
    if what == 'text':    
        
    if what == 'sibling':

succ = 0
fail = 0        
for t in ['a', 'p', 'div']:
    for a in [' href="bla"', ' class="za"', ' id="me"', '']:
        for i in ['', '{}', target, 'nonsense']:
            for o in ['', '{}', target, 'nonsense']: 
                tr.soups = [BeautifulSoup('<{}{}>{}</{}>{}'.format(t, a, i, t, o))] * 2 
                tr.targets = ['bla2','bla2']
                if str(tr.soups[0]).find('bla2'): 
                    if len(buildSolution(tr)) > 0:
                        succ+=1
                        'a'+1
                    else:
                        fail+=1

tr = Training('','')
tr.soups = [BeautifulSoup('<div>text</div>bla'), BeautifulSoup('<div>text</div>bla')]
tr.targets = ['bla', 'bla']

buildSolution(tr)
