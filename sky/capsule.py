import requests
import langdetect
import time
from textblob import TextBlob

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
        
## c = Capsule('http://codigonuevo.com/la-chica-con-la-que-todos-quieren-casarse-pero-con-la-que-nadie-va-salir/')>

try: 
    from .helper import * 
    from .findTitle import getTitle 
    from .get_date import get_publish_from_meta
    from .findBody import getBody 
    from .get_date import get_date_from_content
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
        self.url = 'http://' + url if url.startswith('www') else url
        t1 = time.time()
        self.response = requests.get(self.url)
        t2 = time.time()
        self.html = self.response.text 
        self.tree = makeTree(self.html, self.url) 
        t3 = time.time()
        self.lang = None
        self.publish_date = None
        self.title = None
        self.multiTitle = None
        self.body = None
        self.multiBody = None
        self.img_links = []

        self.source_name = extractDomain(self.url)
        wrong_imgs = ['icon', 'logo', 'advert', 'toolbar', 'footer', 'layout']
        self.img_links = list(set([urljoin(self.source_name, x) for x in self.tree.xpath('//img/@src') 
                                   if not any([w in x for w in wrong_imgs])])) 
        # if development
        self.magic()
        
    def magic(self):
        # Language
        self.body = normalize(normalize(getBody(self.tree)))
        self.body_blob = TextBlob(self.body)
        t1 = time.time()
        # Body
        if self.body:
            self.get_language() 
        # Title
        self.title = getTitle(self.tree)
        t2 = time.time()
        # Date
        self.publish_date = get_publish_from_meta(self.tree) or ''
        t3 = time.time()
        # Entities
        self.entities = extract_entities(self.body_blob)
        t4 = time.time() 

    def get_language(self):
        if 'content-language' in self.response.headers:
            self.lang = self.response.headers['content-language']
            
        if self.lang is None and 'lang' in self.tree.attrib:
            self.lang = self.tree.attrib['lang']

        if self.lang is None:
            self.lang = self.body_blob.detect_language()    
            
        if self.lang is None:
            self.lang = langdetect.detect(self.body)

    def multi(self, tree):
        self.multiTitle = getTitle(prune_first(self.tree, tree))
        self.multiBody = get_first_body(self.tree, tree)

        
            
# c = Capsule('http://mexico.cnn.com/mundo/2014/05/05/por-que-en-eu-celebran-mas-el-5-de-mayo-que-en-mexico-aqui-10-datos')

# c = Capsule('http://www.nieuwsdumper.nl/nieuws/1666/ihi-38n-voor-van-zuijlen.html')

# c1 = Capsule('http://www.bbc.com/news/world-africa-33049312')

# c3 = Capsule('http://www.bbc.com/news/world-asia-china-33044963')






# u1 = 'http://dannorth.net/introducing-bdd/'
# u2 = 'http://dannorth.net/2015/04/24/two-hours-per-team/'

# c1 = Capsule(u1)
# c2 = Capsule(u2)

# ct1 = prune_first(c1.tree, c2.tree)    

# get_first_body(c1.tree, c2.tree)



# it = 0
# it1 = 0
# it2 = 0
# words = []
# for x,y in zip(c.body_blob.words, c.body_blob.translate('nl', 'en').words):
#     it+=1
#     if x.lower() not in stopwords.words('dutch'):
#         it1+=1
#         if y.lower() not in stopwords.words('english'):
#             words.append(y)
            
        

# [x for x in c.body_blob.words if x.lower() not in stopwords.words('dutch')]
