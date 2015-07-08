import requests
import langdetect
from textblob import TextBlob

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
        
## c = Capsule('http://codigonuevo.com/la-chica-con-la-que-todos-quieren-casarse-pero-con-la-que-nadie-va-salir/')>

try: 
    from .helper import * 
    from .findTitle import getTitle 
    from .justy import *
    from .get_date import get_dates
    from .findBody import getBody 
    from .entities import extract_entities
    from .multi import *
except SystemError: 
    from helper import *
    from justy import *
    from findTitle import getTitle 
    from findBody import getBody 
    from get_date import get_dates
    from entities import extract_entities
    from lxmlTree import lxmlTree
    from multi import *

class Capsule():
    def __init__(self, url):
        self.url = 'http://' + url if url.startswith('www') else url
        if url.startswith('file://'):
            with open(url[7:]) as f:
                self.response = None
                self.html = f.read()
        else:        
            self.response = requests.get(self.url)
            self.html = self.response.text 
        self.lang = None
        self.publish_date = None
        self.title = None
        self.multiTitle = None
        self.body = None
        self.body_blob = None
        self.multiBody = None
        self.multiBodyBlob = None
        self.img_links = []
        self.entities = []
        self.source_name = extractDomain(self.url) 
        self.multi_publish_date = None 
        self.jt = None
        
    def single_magic(self, method = 'justext'):
        # Language
        tree = makeTree(self.html, self.url)  
        if method == 'justext':
            try:
                self.get_language(tree)
            except:
                self.lang = 'en' 
            self.jt = justy(self.html, self.lang)
            self.title = justyTitle(self.jt)
            self.title = justyBody(self.jt)
        else: 
            self.body = normalize(normalize(getBody(tree)))
            
            if self.body:
                self.get_language(tree) 

            self.title = getTitle(tree)
            
        wrong_imgs = ['icon', 'logo', 'advert', 'toolbar', 'footer', 'layout']
        self.img_links = list(set([urljoin(self.source_name, x) for x in tree.xpath('//img/@src') 
                                   if not any([w in x for w in wrong_imgs])])) 
        self.body_blob = TextBlob(self.body)

        
        self.publish_date = ''
        for date_group in get_dates(tree, self.lang):
            if date_group:
                self.publish_date = str(date_group[0])

        self.entities = extract_entities(self.body_blob)

    def get_language(self, tree):
        if self.response and 'content-language' in self.response.headers:
            self.lang = self.response.headers['content-language']
            
        if self.lang is None and 'lang' in tree.attrib:
            self.lang = tree.attrib['lang']

        if self.response and self.lang is None:
            self.lang = self.body_blob.detect_language()    
            
        if self.lang is None:
            self.lang = langdetect.detect(self.body)

    def multi_magic(self, most_similar_tree):
        import textblob
        this_tree = prune_first(makeTree(self.html, self.url), most_similar_tree)  
        self.multiTitle = getTitle(this_tree)
        self.multiBody = get_multi_body(this_tree)
        self.multiBodyBlob = textblob.TextBlob(self.multiBody) 
        self.multi_publish_date = get_publish_from_meta(this_tree) or ''

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

