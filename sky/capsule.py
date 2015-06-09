import requests
import langdetect
import time
from textblob import TextBlob

## c = Capsule('http://codigonuevo.com/la-chica-con-la-que-todos-quieren-casarse-pero-con-la-que-nadie-va-salir/')>

try: 
    from .helper import * 
    from .findTitle import getTitle 
    from .get_date import get_publish_from_meta
    from .findBody import getBody 
    from get_date import get_date_from_content
    from .entities import extract_entities
except SystemError: 
    from helper import *
    from findTitle import getTitle 
    from findBody import getBody 
    from get_date import get_publish_from_meta
    from get_date import get_date_from_content
    from entities import extract_entities
    from lxmlTree import lxmlTree

class Capsule():
    def __init__(self, url):
        self.url = url
        t1 = time.time()
        self.response = requests.get(url)
        t2 = time.time()
        self.html = self.response.text 
        self.tree = makeTree(self.html, url) 
        t3 = time.time()
        self.lang = None
        self.publish_date = None
        self.title = None
        self.body = None
        print('t2 {} t3 {}'.format(t2 - t1, t3 - t2))

        # if development
        self.magic()
        
    def magic(self):
        # Language
        self.body = normalize(normalize(getBody(self.tree)))
        self.body_blob = TextBlob(self.body)
        t1 = time.time()
        # Body
        self.get_language() 
        # Title
        self.title = getTitle(self.tree)
        t2 = time.time()
        # Date
        self.publish_date = get_publish_from_meta(self.tree) or None
        t3 = time.time()
        # Entities
        self.entities = extract_entities(self.body_blob)
        t4 = time.time()
        print('t2 {} t3 {} t4 {}'.format(t2 - t1, t3 - t2, t4 - t3))
        
    def get_language(self):
        if 'content-language' in self.response.headers:
            self.lang = self.response.headers['content-language']
            
        if self.lang is None and 'lang' in self.tree.attrib:
            self.lang = self.tree.attrib['lang']

        if self.lang is None:
            self.lang = self.body_blob.detect_language()    
            
        if self.lang is None:
            self.lang = langdetect.detect(self.body)

c = Capsule('http://mexico.cnn.com/mundo/2014/05/05/por-que-en-eu-celebran-mas-el-5-de-mayo-que-en-mexico-aqui-10-datos')

c = Capsule('http://www.nieuwsdumper.nl/nieuws/1666/ihi-38n-voor-van-zuijlen.html')

c1 = Capsule('http://www.bbc.com/news/world-africa-33049312')
c2 = Capsule('http://www.bbc.com/news/world-asia-china-33044963')

removers = []
for x in c.tree.xpath('//body')[0].iter():
    if not normalize(x.text_content()).strip():
        removers.append(x)
        
while removers:
    try:
        ele = removers.pop()        
        ele.getparent().remove(ele)
    except IndexError:
        pass

t = list(c.tree.xpath('//body')[0].iter())

def addDepth(node, depth = 0):
    node.depth = depth
    for n in node.iterchildren():
        if hasattr(n, 'iterchildren'):
            addDepth(n, depth + 1)

addDepth(t[0])
            
dictree = {}            

lxmlTree(t[0].xpath('//div[@class="menumobile"]'))

view_node(t[0].xpath('//div[@class="menumobile"]')[0])





it = 0
it1 = 0
it2 = 0
words = []
for x,y in zip(c.body_blob.words, c.body_blob.translate('nl', 'en').words):
    it+=1
    if x.lower() not in stopwords.words('dutch'):
        it1+=1
        if y.lower() not in stopwords.words('english'):
            words.append(y)
            
        

[x for x in c.body_blob.words if x.lower() not in stopwords.words('dutch')]
