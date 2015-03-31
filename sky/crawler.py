from ZODB.FileStorage import FileStorage
from ZODB.DB import DB

import transaction
import persistent
import time

from selenium import webdriver

import requests


try: 
    from queue import Queue
    from queue import PriorityQueue
except ImportError: 
    from Queue import PriorityQueue



storage = FileStorage('Data.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

class RequestsCrawler():
    def __init__(self, name, backend = None): 
        self.name = name
        self.backend = backend
        
    def get(self, url):
        response = requests.get(url)
        html = response.text
        return html
        

class SeleniumCrawler():
    def __init__(self, name, backend):
        self.name = name
        self.browser = backend
        self.active = True
        self.min_time = 2

    def start(self):
        t2 = 0
        while self.active: 
            t1 = time.time()
            if t2 - t1 > self.min_time:
                self.get()
                t2 = time.time()
            
            
        
    def get(self, url):
        self.browser.get(url)
        html = self.browser.page_source
        return html

class BeautifulSoupParser():
    

class Parser():
    def __init__(self, backend): 
        self.backend = backend
    def parse(self): 
        
        return parsedDocument

class CrawlerManager():
    def __init__(self):
        self.crawlers = []
        self.urlQueue = PriorityQueue()

    def registerCrawler(self, crawler):
        self.crawlers.append(crawler)

    def ask(self):
        url = self.urlQueue.get()
        
        
