import requests
from helper import *
import langdetect

from get_date import get_publish_from_meta

class Capsule():
    def __init__(self, url):
        self.url = url
        self.response = requests.get(url)
        self.html = self.response.text 
        self.tree = makeTree(self.html, url) 
        self.lang = None
        self.publish_date = None
        
    def magic(self):
        # Language
        self.get_language() 

        # Date
        self.publish_date = get_publish_from_meta(self.tree) or None
        
    def get_language(self):
        if 'content-language' in self.response.headers:
            self.lang = self.response.headers['content-language']
            
        if self.lang is None and 'lang' in self.tree.attrib:
            self.lang = self.tree.attrib['lang']

        if self.lang is None:
            self.lang = langdetect.detect(self.html)
            
            

r = Capsule('https://pypi.python.org/pypi/capsule')
