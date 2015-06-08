import requests
import langdetect
import nltk
import time

try: 
    from .helper import * 
    from .findTitle import getTitle 
    from .get_date import get_publish_from_meta
    from .findBody import getBody 
    from .entities import extract_entities
except SystemError: 
    from helper import *
    from findTitle import getTitle 
    from findBody import getBody 
    from get_date import get_publish_from_meta
    from entities import extract_entities

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
        self.entities = extract_entities(self.body)
        t4 = time.time()
        print('t2 {} t3 {} t4 {}'.format(t2 - t1, t3 - t2, t4 - t3))
        
    def get_language(self):
        if 'content-language' in self.response.headers:
            self.lang = self.response.headers['content-language']
            
        if self.lang is None and 'lang' in self.tree.attrib:
            self.lang = self.tree.attrib['lang']

        if self.lang is None:
            self.lang = langdetect.detect(self.body)

c = Capsule('http://mexico.cnn.com/mundo/2014/05/05/por-que-en-eu-celebran-mas-el-5-de-mayo-que-en-mexico-aqui-10-datos')
