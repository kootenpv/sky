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

class Crawler():
    def __init__(self, name, queue):
        self.name = name
        self.backend = requests
        self.active = True
        self.min_time = 2
        self.queue = queue
        self.active = True

    def get(self, url):
        pass
        
    def start(self):
        t2 = 0
        while self.active: 
            t1 = time.time()
            print(t2, t1)
            if t1 - t2 > self.min_time:
                if self.queue:
                    url = self.queue.pop()
                    print("name {} num chars {} time waited {}".format(self.name, len(self.get(url)), t2 - t1))
                    t2 = time.time() 
                    transaction.commit()
            else:
                time.sleep(0.5)    
                
    def stop(self):
        self.active = False
        if hasattr(self.backend, 'close'):
            self.backend.close()

class RequestsCrawler(Crawler):        
    def get(self, url):
        response = requests.get(url)
        html = response.text
        return html

class SeleniumCrawler(Crawler): 
    def __init__(self, name, queue, backend = webdriver.Firefox):
        super().__init__(name, queue)
        self.backend = backend()
    def get(self, url):
        self.backend.get(url)
        html = self.backend.page_source
        return html

class BeautifulSoupParser():
    pass
    

class Parser():
    def __init__(self, backend): 
        self.backend = backend
    def parse(self): 
        
        return parsedDocument

class CrawlerManager():
    def __init__(self):
        self.crawlers = []
        self.queue = []

    def registerCrawler(self, crawler):
        self.crawlers.append(crawler)

    def startCrawlers(self):
        for crawler in self.crawlers:
            crawler.start()
            
    def stopCrawlers(self, force = False):
        for crawler in self.crawlers:
            crawler.stop()        
            
    def startNaive(self, urls):
        self.queue.extend(urls)
        self.registerCrawler(SeleniumCrawler('selenium1', self.queue, webdriver.PhantomJS))
        self.registerCrawler(RequestsCrawler('requests1', self.queue))


cm = CrawlerManager()

cm.startNaive(['http://www.nieuwsdumper.nl/nieuws']*10)

cm.startCrawlers()

