import sys
import os
import mechanize
import urllib
from bs4 import BeautifulSoup
import re
import time
import random
import urlparse
import signal
import selenium.webdriver
import codecs


class SkyScraper():

    def __init__(self, config):
        self.CONFIG = config
        self.num_done = 0

    def write_queue(self, queue):
        with open(self.CONFIG['collections_path'] + self.CONFIG['collection_name'] + '.queue', 'w') as f:
            f.write("\n".join(queue))
        sys.exit(0)

    def shouldCrawl(self, url):
        if all([x not in url for x in self.CONFIG['crawlFilterStrings']]):
            if any([x in url for x in self.CONFIG['crawlRequiredStrings']]):
                return True
        return False

    def shouldIndex(self, url):
        if all([x not in url for x in self.CONFIG['indexFilterStrings']]):
            if (any([condition in url for condition in self.CONFIG['indexRequiredStrings']]) or not self.CONFIG['indexRequiredStrings']):
                return True
        return False

    def crawl(self, webCrawler, queue, done):
        try:
            index = []
            if 'mechanize' in webCrawler.__module__:
                links = [link.url for link in webCrawler.links()]
            elif 'selenium' in webCrawler.__module__:
                links = [link.get_attribute('href')
                         for link in webCrawler.find_elements_by_xpath("//*[@href]")]
            for link in links:
                url = urlparse.urljoin(self.CONFIG['host'], link)
                if self.CONFIG['host'] not in url:
                    continue
                if (url not in done) & (url not in queue):
                    # index
                    if self.shouldIndex(url):
                        self.log_url(url)
                        if self.CONFIG['writeHTML']:
                            index.append(url)
                    # crawl
                    if self.shouldCrawl(url):
                        queue.append(url)
        except Exception as e:
            print(e)
            if 'mechanize' in webCrawler.__module__:
                print "error", webCrawler.geturl()
            elif 'selenium' in webCrawler.__module__:
                print "error", webCrawler.current_url
        for url in index:
            self.save_response(webCrawler, url)
        return queue

    def log_url(self, url):
        with open(self.CONFIG['collections_path'] + self.CONFIG['collection_name'] + '.urls', 'a') as f:
            f.write(url + '\n')

    def log_error(self, url, e):
        with open(self.CONFIG['collections_path'] + self.CONFIG['collection_name'] + '.errorurls', 'a') as f:
            f.write(e + ": " + url + '\n')

    def save_response(self, webCrawler, url):
        # Handle response
        if 'mechanize' in webCrawler.__module__:
            response = webCrawler.open(url)
            webCrawler._factory.is_html = True
            responseHeader = str(response.info())
            html_response = response.read()
        elif 'selenium' in webCrawler.__module__:
            webCrawler.get(url)
            responseHeader = 'simple'
            html_response = webCrawler.page_source
        fname = urllib.url2pathname(url).split('/')[-1]
        if ('.' not in fname) | ('.ashx' in fname) | ('.aspx' in fname):
            if 'msword' in responseHeader:
                extension = '.doc'
            elif 'pdf' in responseHeader:
                extension = '.pdf'
            elif 'excel' in responseHeader:
                print "RESP", responseHeader
                extension = '.xls'
            elif 'powerpoint' in responseHeader:
                extension = '.ppt'
            elif 'text/html' in responseHeader:
                extension = '.aspx'
            else:
                extension = ''
            fname = ".".join(fname.split('.')[:-1]) + extension
        else:
            extension = '.html'

        save_location = url.replace(self.CONFIG['host'], self.CONFIG['collections_path'] +
                                    self.CONFIG['collection_name'] + '/' +
                                    self.CONFIG['collection_name'])
        save_location.replace('//', '/')
        save_location = re.sub('[^a-zA-Z0-9_/-]', "", save_location)
        save_location = "/".join(save_location.split("/")[:-1]) + "/"
        if not os.path.exists(save_location):
            os.makedirs(save_location)
        binaryExtensions = ['.pdf', '.doc', '.xlsx', '.ppt', '.aspx']
        if extension in binaryExtensions:
            with open(save_location + fname.replace('.aspx', '.html'), "wb") as f:
                f.write(html_response)
                print "written " + save_location + fname
        else:
            with codecs.open(save_location + fname, "w", 'utf-8-sig') as f:
                f.write(html_response)
                print "written " + save_location + fname
        self.num_done += 1

    def continue_from_log(self):
        fname = self.CONFIG['collections_path'] + self.CONFIG['collection_name'] + '.urls'
        if os.path.exists(fname):
            with open(fname) as f:
                done_so_far = f.read().strip().split('\n')
                print "done_so_far:", len(done_so_far)
                return done_so_far
        else:
            with open(fname, 'w') as f:
                f.write('')
            return []

    def continue_from_queue(self):
        fname = self.CONFIG['collections_path'] + self.CONFIG['collection_name'] + '.queue'
        if os.path.exists(fname):
            with open(fname) as f:
                queue = f.read().strip().split('\n')
                print "queue_len:", len(queue)
                return queue
        else:
            with open(fname, 'w') as f:
                f.write('')
            print "starting from:", self.CONFIG['startURLs']
            return self.CONFIG['startURLs']

    def scrape(self):
        self.validate_config()

        if self.CONFIG['browser'] == 'M':
            webCrawler = mechanize.Browser()
            webCrawler.set_handle_robots(False)
            loginInfoFields = ['usernameField', 'usernameValue',
                               'passwordField', 'passwordValue', 'loginURL']
            if any([field in self.CONFIG for field in loginInfoFields]):
                if not all([field in self.CONFIG for field in loginInfoFields]):
                    raise Exception("")
                webCrawler.open(self.CONFIG['loginURL'])
                webCrawler.select_form(nr=0)
                webCrawler.form[self.CONFIG['usernameField']] = self.CONFIG['usernameValue']
                webCrawler.form[self.CONFIG['passwordField']] = self.CONFIG['passwordValue']
                res = webCrawler.submit()
                print webCrawler.open(self.CONFIG['host']).read()

        elif self.CONFIG['browser'] == 'S':
            path_to_chromedriver = '/Users/pascal/Downloads/chromedriver'
            webCrawler = selenium.webdriver.Chrome(executable_path=path_to_chromedriver)

            # Nice login handling FOR PORTAL MEDIQ
            # webCrawler.get('https://portal.mediq.nl/login.aspx')
            # z = raw_input('Waiting for filling in Login. Hit ENTER')

        self.makeStandardizedBrowser(webCrawler)

        # Lists that contain the URLs that were visited and those that are still enqueued
        done = self.continue_from_log()
        queue = self.continue_from_queue()

        self.num_done = len(done)

        while queue and self.num_done < self.CONFIG['maximum_number_of_documents']:
            random.shuffle(queue)
            try:
                url = urlparse.urljoin(self.CONFIG['host'], queue.pop(0))
                if url:
                    signal.signal(signal.SIGINT, lambda s, f: self.write_queue(queue))
                    if url in done:
                        print "ALREADY DONE", url
                        continue

                    logString = "done: " + str(len(set(done))) + " left: " + \
                        str(len(queue)) + " now: " + url

                    if self.CONFIG['browser'] == 'S':
                        webCrawler.get(url)
                    else:
                        webCrawler.open(url)

                    queue = self.crawl(webCrawler, queue, done)

                done.append(url)
                print logString
            except Exception as e:
                self.log_error(url, str(e))
                with open(self.CONFIG['collections_path'] + self.CONFIG['collection_name'] + '.queue', 'w') as f:
                    f.write("\n".join(queue))
                print str(e), ':', url
            time.sleep(self.CONFIG['wait_between_url_visits_in_seconds'])

    def makeStandardizedBrowser(self, browserObj):
        if isinstance(browserObj, mechanize.Browser):
            browserObj.addheaders = [('User-agent', 'Jibes WatsonBot (+pvkooten@jibes.nl)')]

    def validate_config(self):
        required = ['host', 'collections_path', 'collection_name', 'startURLs',
                    'crawlFilterStrings', 'crawlRequiredStrings', 'indexFilterStrings', 'indexRequiredStrings']
        missing = []
        for x in required:
            if x not in self.CONFIG:
                missing.append(x)
        self.CONFIG['crawlFilterStrings'].extend(['.jpeg', '.jpg', '#'])
        self.CONFIG['indexFilterStrings'].extend(['.jpeg', '.jpg', '#'])
        if missing:
            raise Exception("Missing REQUIRED parameter(s): " + ", ".join(missing))
        optional = {'maximum_number_of_documents': 10000,
                    'wait_between_url_visits_in_seconds': 1,
                    'writeHTML': True,
                    'browser': 'M'}
        for x in optional:
            if x not in self.CONFIG:
                self.CONFIG[x] = optional[x]
