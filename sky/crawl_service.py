from sky.crawler_plugins import CrawlCloudantPluginNews
from sky.crawler_plugins import CrawlZODBPluginNews
from sky.crawler_plugins import CrawlElasticSearchPluginNews
import cloudant
from elasticsearch import Elasticsearch

class CrawlService():
    def __init__(self, project_name): 
        self.project_name = project_name 
        self.plugins = {}
        self.server = None
        self.get_server()
        self.get_crawl_plugins()

    def get_server(self):
        raise NotImplementedError("get_server not implemented")

    def get_crawl_plugins(self): 
        raise NotImplementedError("get_crawl_plugins not implemented")

    def get_crawl_plugin(self, plugin_name, crawl_plugin_class):
        return crawl_plugin_class(self.project_name, self.server, plugin_name) 

    def run(self, plugin_name, crawl_plugin_class):
        cplug = self.get_crawl_plugin(plugin_name, crawl_plugin_class)
        cplug.run()

    def run_all(self, crawl_plugin_class): 
        for plugin in self.plugins: 
            crawl_plugin_class(plugin, self.server).run()

class CrawlCloudantService(CrawlService):
    def __init__(self, project_name): 
        super(CrawlCloudantService, self).__init__(project_name) 
        self.crawler_plugins_db = None

    def get_server(self):
        with open('cloudant.username') as f:
            USERNAME = f.read()    
        with open('cloudant.password') as f:
            PASSWORD = f.read() 
        account = cloudant.Account(USERNAME)
        account.login(USERNAME, PASSWORD) 

        # create dbs if they don't exist
        account.database(self.project_name + '-crawler-plugins').put()
        account.database(self.project_name + '-crawler-documents').put()
        account.database(self.project_name + '-crawler-template_dict').put()

        self.server = account
                
    def get_crawl_plugins(self): 
        plugin_db = self.server.database(self.project_name + '-crawler-plugins')
        db_uri = '{}/_all_docs?include_docs=true'.format(plugin_db.uri)
        service_rows = plugin_db.get(db_uri).json()['rows']
        self.plugins = {row['doc']['plugin_name'] : row['doc'] for row in service_rows 
                        if 'default' != row['doc']['plugin_name']}


class CrawlZODBService(CrawlService):
    from ZODB.FileStorage import FileStorage
    from ZODB.serialize import referencesf
    from ZODB.DB import DB
    import transaction
    from BTrees.OOBTree import OOBTree
    import time
    
    def __init__(self, project_name): 
        super(CrawlZODBService, self).__init__(project_name) 

    def get_server(self):
        # In services, a FileStorage (or perhaps other backend) object has to be provided
        fname = '/Users/pascal/GDrive/sky_collections/zodbtest/{}.fs'.format(self.project_name)
        self.storage = self.FileStorage(fname)
        db = self.DB(self.storage)
        connection = db.open()
        self.server = connection.root()

        # create dbs if they don't exist
        tables = ['plugins', 'documents', 'template-dict']
        for table in tables:
            if table not in self.server:
                self.server[table] = self.OOBTree() 
                self.transaction.commit()

    def pack(self):
        self.storage.pack(self.time.time(), self.referencesf) 
        
    def get_crawl_plugins(self): 
        return {k : doc for k, doc in self.server['plugins'].items()
                if k != 'default'}

# cfs = CrawlFileService('/Users/pascal/GDrive/raboleadcrawl/')
# cfs.run()
