from sky.crawl_plugin import CrawlFilePlugin
from sky.crawl_plugin import CrawlCloudantPlugin
import os
import cloudant

class CrawlService():
    def __init__(self, location, crawl_plugin): 
        self.location = location
        self.cp = crawl_plugin
        self.plugins = []

    def login(self):
        # If needed, make sure crawler is logged in and ready to write
        pass

    def get_crawl_plugins(self): 
        # Obtain crawler plugins
        pass

    def run(self):
        self.login()
        self.plugins = self.get_crawl_plugins()
        for plugin in self.plugins:
            cplug = self.cp(plugin['plugin_name']) 
            cplug.run()

class CrawlFileService(CrawlService):
    def __init__(self, file_location): 
        super(CrawlFileService, self).__init__(file_location, CrawlFilePlugin) 
        
    def get_crawl_plugins(self): 
        os.chdir(self.location)
        plugins = []
        for name in os.listdir(): 
            if any([x in name for x in ['.DS_STORE', '#', '.py', 'results_', 'done_']]): 
                continue 
            plugins.append(
                {'plugin_name' : name,
                 'last_crawled' : '20150101T15:30+00:00',
                 'number_of_new_urls' : 15,
                 'pagination_urls' : []
                 }) 
        return plugins

class CrawlCloudantService(CrawlService):
    def __init__(self, table): 
        super(CrawlCloudantService, self).__init__(table, CrawlCloudantPlugin) 
        self.crawler_services_db = None

    def login(self):
        with open('cloudant.username') as f:
            USERNAME = f.read()    
        with open('cloudant.password') as f:
            PASSWORD = f.read() 
        account = cloudant.Account(USERNAME)
        account.login(USERNAME, PASSWORD)
        self.crawler_services_db = account.database(self.location)
    
    def get_crawl_plugins(self): 
        # Needs to send the whole status for consideration
        db_uri = '{}/_all_docs?include_docs=true'.format(self.crawler_services_db.uri)
        service_rows = self.crawler_services_db.get(db_uri).json()['rows']
        return [row['doc'] for row in service_rows]

# cfs = CrawlFileService('/Users/pascal/GDrive/raboleadcrawl/')
# cfs.run()

# ccs = CrawlCloudantService('crawler-services')
# ccs.run()
