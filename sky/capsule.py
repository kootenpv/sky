import requests
import langdetect

try:
    from .get_date import get_publish_from_meta
    from .helper import * 
    from .findTitle import getTitle 
except SystemError:
    from get_date import get_publish_from_meta
    from helper import *
    from findTitle import getTitle 

class Capsule():
    def __init__(self, url):
        self.url = url
        self.response = requests.get(url)
        self.html = self.response.text 
        self.tree = makeTree(self.html, url) 
        self.lang = None
        self.publish_date = None
        self.title = None
        self.body = None

        # if development
        self.magic()
        
    def magic(self):
        # Language
        self.get_language() 

        # Body

        # Title
        self.title = getTitle(self.tree)
        # Date
        self.publish_date = get_publish_from_meta(self.tree) or None

    def get_language(self):
        if 'content-language' in self.response.headers:
            self.lang = self.response.headers['content-language']
            
        if self.lang is None and 'lang' in self.tree.attrib:
            self.lang = self.tree.attrib['lang']

        if self.lang is None:
            self.lang = langdetect.detect(self.html)                 

c = Capsule('http://mexico.cnn.com/mundo/2014/05/05/por-que-en-eu-celebran-mas-el-5-de-mayo-que-en-mexico-aqui-10-datos')


