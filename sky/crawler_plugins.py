### split into separate files for DBs, or should I?

## Take care of backend for handle results
## for new project
# Create the databases
# Create the "default" document in plugins
# Create the design document        

import json
from sky.configs import DEFAULT_CRAWL_CONFIG
from sky.scraper import Scrape
from sky.crawler import crawl
from sky.crawler.crawling import NewsCrawler
from sky.helper import slugify

class CrawlPlugin():
    def __init__(self, plugin_name):
        self.plugin_name = plugin_name 
        self.crawl_config = None
        self.scrape_config = None
        self.data = {}
        self.documents = []
        self.template_dict = None

    def get_default_plugin(self):
        pass

    def apply_specific_plugin(self):
        pass

    def get_scrape_config(self):    
        scrape_config = self.crawl_config.copy()

        
        scrape_config.update({ 
            'template_proportion' : 0.09,
            'max_templates' : 1000
        })

        return scrape_config

    def start_crawl(self):
        crawl.start(self.crawl_config)
    
    def scrape_data(self):
        # Create boilerplate recognizer
        skindex = Scrape(self.scrape_config)

        # Process all by removing boilerplate and extracting information
        return skindex.process_all(exclude_data = ['cleaned', 'author'])

    def get_documents(self, maximum_number_of_documents = 10000):
        pass

    def handle_results(self, to = None):
        pass

    def run(self, use_cache = False):
        self.crawl_config = self.get_default_plugin()
        self.apply_specific_plugin()
        self.scrape_config = self.get_scrape_config()
        if not use_cache:
            self.start_crawl()
        self.data = self.scrape_data()
        self.handle_results()

    def get_bad_summary(self, force_get_documents = False, n = 5):
        if not self.documents or force_get_documents:
            self.documents = self.get_documents()
        title_sort = sorted(self.documents, key = lambda doc: len(doc['title']))
        body_sort = sorted(self.documents, key = lambda doc: len(' '.join(doc['body'])))
        date_sort = sorted(self.documents, key = lambda doc: len(doc['publish_date']))
        url_sort = sorted(self.documents, key = lambda doc: len(doc['url']))
        return {k :[(d['url'], d[k]) for d in sorted_type][:n] 
                for k, sorted_type in zip(['title', 'body', 'publish_date', 'url'], 
                                          [title_sort, body_sort, date_sort, url_sort])}

class CrawlFilePlugin(CrawlPlugin):
    def __init__(self, plugin_name): 
        super(CrawlFilePlugin, self).__init__(plugin_name)

    def get_default_plugin(self): 
        return DEFAULT_CRAWL_CONFIG
        
    def apply_specific_plugin(self):
        with open(self.plugin_name) as f:
            specific_config = json.load(f)
        self.crawl_config.update(specific_config)        
        
    def handle_results(self, to = "file"):
        with open('results_{}.json'.format(self.plugin_name), 'w') as f:
            json.dump(self.data, f)

class CrawlCloudantPlugin(CrawlPlugin):
    ### 
    # Make it so that the service can do the login once, and that this receives the databases 
    ### 
    # Class import
    import cloudant
    def __init__(self, plugin_name): 
        super(CrawlCloudantPlugin, self).__init__(plugin_name) 
        self.crawler_plugins_db = None
        self.crawler_documents_db = None
        self.login()

    def login(self):
        with open('cloudant.username') as f:
            USERNAME = f.read()
        with open('cloudant.password') as f:
            PASSWORD = f.read()
        account = self.cloudant.Account(USERNAME)
        account.login(USERNAME, PASSWORD)
        self.crawler_plugins_db = account.database('crawler-plugins-test') 
        self.crawler_documents_db = account.database('crawler-documents-test')
        self.crawler_template_db = account.database('crawler-template-dict-test')
        # create dbs if they don't exist
        self.crawler_plugins_db.put()
        self.crawler_documents_db.put()
        self.crawler_template_db.put()
        

    def get_default_plugin(self): 
        return self.crawler_plugins_db.get('default').json()
        
    def apply_specific_plugin(self): 
        plugin = self.crawler_plugins_db.get(self.plugin_name).json()
        self.crawl_config.update(plugin)
        seen_urls = self.get_seen_urls()
        self.crawl_config['seen_urls'] = seen_urls
        
    def handle_results(self, to = "cloudant"): 
        if to == "cloudant":
            for url_id in self.data: 
                self.data[url_id]['_id'] = slugify(url_id)
            self.crawler_documents_db.bulk_docs(*list(self.data.values()))

    def get_documents(self, maximum_number_of_documents = 1000000): 
        # now just to add the host thing ??????????????
        query = 'query={}'.format(self.plugin_name)
        params = '?include_docs=true&limit={}&{}'.format(maximum_number_of_documents, query) 
        return [x['doc'] for x in self.crawler_documents_db.all_docs().get(params).json()['rows']
                if self.plugin_name in x['doc']['url']]

    def get_seen_urls(self): 
        params = '?query={}'.format(self.plugin_name) 
        udocs = self.crawler_documents_db.design('urlview').view('view1').get(params).json()['rows']
        return set([udoc['key'] for udoc in udocs])
        
    def save_config(self, config):
        doc = self.crawler_plugins_db.get(self.plugin_name).json()
        if 'error' in doc:
            doc = {}
        doc.update(config) 
        self.crawler_plugins_db[self.plugin_name] = doc

class CrawlElasticSearchPlugin(CrawlPlugin):
    ### 
    # Make it so that the service can do the login once, and that this receives the databases 
    ###
    ### Class import
    from elasticsearch import Elasticsearch
    import elasticsearch
    def __init__(self, plugin_name): 
        super(CrawlElasticSearchPlugin, self).__init__(plugin_name)
        self.crawler_plugins_db = None
        self.crawler_documents_db = None
        self.plugins = []
        self.login()

    def login(self): 
        self.es = self.Elasticsearch([{'host': 'localhost', 'port': 9200}]) 
        self.create_index_if_not_existent('crawler-documents')
        self.create_index_if_not_existent('crawler-plugins')
        self.create_index_if_not_existent('crawler-services')
        self.create_index_if_not_existent('crawler-template-dict')
        
    def create_index_if_not_existent(self, name, request_body = None): 
        if not self.es.indices.exists(name):
            if request_body is None:
                request_body = {
                    "settings" : {
                        "number_of_shards": 1,
                        "number_of_replicas": 0
                    }
                }
            self.es.indices.create(index = name, body = request_body)

    def get_default_plugin(self): 
        return self.es.get(index = "crawler-plugins", doc_type = 'plugin', id = 'default')['_source']
        
    def apply_specific_plugin(self): 
        conf = self.es.get(index = "crawler-plugins", doc_type = 'plugin', id = self.plugin_name)['_source']
        self.crawl_config.update(conf)        
        seen_urls = self.get_seen_urls()
        self.crawl_config['seen_urls'] = seen_urls
        
    def handle_results(self, to = "cloudant"): 
        for url_id in self.data: 
            doc_id = slugify(url_id) 
            self.es.index(index = "crawler-documents", doc_type = 'document', 
                          id = doc_id, body = self.data[url_id])
        print(to)    

    def get_documents(self, maximum_number_of_documents = 1000000): 
        query = {"query": {"wildcard": {"url": "*{}*".format(self.plugin_name)}}}
        res = self.es.search(index = "crawler-documents", doc_type = 'document', body = query)
        return res['hits']['hits']

    def get_seen_urls(self): 
        query = {"query": {"wildcard": {"url": "*{}*".format(self.plugin_name)}}, "fields" : "url"}        
        res = self.es.search(index = "crawler-documents", doc_type = 'document', body= query)
        return set([x['fields']['url'][0] for x in res['hits']['hits']])
        
    def save_config(self, config):
        self.es.index(index = "crawler-plugins", doc_type = 'plugin', id = self.plugin_name, body = config)

class CrawlZODBPlugin(CrawlPlugin):
    ### 
    # Make it so that the service can do the login once, and that this receives the databases 
    ###

    # Class  imports
    from ZODB.FileStorage import FileStorage
    from ZODB.serialize import referencesf
    from ZODB.DB import DB
    import transaction
    from BTrees.OOBTree import OOBTree
    import time

    def __init__(self, plugin_name): 
        super(CrawlZODBPlugin, self).__init__(plugin_name) 
        self.root = None
        self.storage = None
        self.login()

    def login(self): 
        # In services, a FileStorage (or perhaps other backend) object has to be provided
        self.storage = self.FileStorage('/Users/pascal/GDrive/sky_collections/zodbtest/Data.fs')
        db = self.DB(self.storage)
        connection = db.open()
        self.root = connection.root()
        tables = ['crawler-plugins', 'crawler-documents', 'crawler-services', 'crawler-template-dict']
        for table in tables:
            if table not in self.root:
                self.root[table] = self.OOBTree() 
                self.transaction.commit()

    def get_default_plugin(self): 
        return self.root['crawler-plugins']['default']
        
    def apply_specific_plugin(self): 
        conf = self.root['crawler-plugins'][self.plugin_name]
        self.crawl_config.update(conf)        
        seen_urls = self.get_seen_urls()
        self.crawl_config['seen_urls'] = seen_urls
        
    def handle_results(self, to = "cloudant"): 
        for url_id in self.data: 
            self.root['crawler-documents'][slugify(url_id)] = self.data[url_id]
        self.transaction.commit()
        print(to)    

    def get_documents(self, maximum_number_of_documents = 1000000): 
        return self.root['crawler-documents']

    def get_seen_urls(self): 
        return set([self.root['crawler-documents'][s]['url'] for s in self.root['crawler-documents'] 
                    if self.plugin_name in self.root['crawler-documents'][s]['url']]) 
        
    def save_config(self, config):
        self.root['crawler-plugins'][self.plugin_name] = config
        self.transaction.commit()

    def pack(self):
        self.storage.pack(self.time.time(), self.referencesf)        

class CrawlPluginNews(CrawlPlugin):
    import ast
    def save_data_while_crawling(self, data):
        raise NotImplementedError('save_data_while_crawling required')
        
    def get_template_dict(self):
        raise NotImplementedError('get_template_dict required')

    def save_template_dict(self, templated_dict):
        raise NotImplementedError('save_template_dict required')
        
    def run(self, use_cache = False):
        self.crawl_config = self.get_default_plugin()
        self.apply_specific_plugin()
        self.scrape_config = self.get_scrape_config() 
        self.scrape_config['template_dict'] = self.get_template_dict()
        # separate out the save data while crawling and the newscraler
        templated_dict = crawl.start(self.scrape_config, NewsCrawler, self.save_data_while_crawling) 
        self.save_template_dict(templated_dict)
    
        
class CrawlZODBPluginNews(CrawlZODBPlugin, CrawlPluginNews): 

    def save_data_while_crawling(self, data): 
        self.root['crawler-documents'][slugify(data['url'])] = data
        self.transaction.commit()

    def get_template_dict(self):
        if ('crawler-template-dict' not in self.root and 
            self.plugin_name not in self.root['crawler-template-dict']): 
            template_dict = self.OOBTree()
        else:
            template_dict = self.root['crawler-template-dict'][self.plugin_name]
        return template_dict

    def save_template_dict(self, templated_dict):
        if templated_dict:
            self.root['crawler-template-dict'][self.plugin_name] = self.OOBTree(templated_dict)
            self.transaction.commit()


class CrawlElasticSearchPluginNews(CrawlElasticSearchPlugin, CrawlPluginNews): 

    def save_data_while_crawling(self, data): 
        self.es.index(index = "crawler-documents", doc_type = 'document', 
                      id = slugify(data['url']), body = data) 

    def get_template_dict(self):
        try:
            template_dict = self.es.get(index = "crawler-template-dict", doc_type = 'template-dict', 
                                        id = self.plugin_name)['_source']
            template_dict = {self.ast.literal_eval(k) : v for k,v in template_dict.items()}
        except self.elasticsearch.NotFoundError:
            template_dict = {}
        return template_dict

    def save_template_dict(self, templated_dict):
        if templated_dict:
            try:
                self.es.index(index = "crawler-template-dict", doc_type = 'template-dict', id = self.plugin_name, 
                               body = json.dumps({repr(k): v for k, v in templated_dict.items()}))
            except self.elasticsearch.RequestError: 
                self.es.update(index = "crawler-template-dict", doc_type = 'template-dict', id = self.plugin_name, 
                               body = json.dumps({"doc" : {repr(k): v for k, v in templated_dict.items()}}))

class CrawlCloudantPluginNews(CrawlCloudantPlugin, CrawlPluginNews): 

    def save_data_while_crawling(self, data): 
        self.crawler_documents_db[slugify(data['url'])] = data

    def get_template_dict(self): 
        template_dict = self.crawler_template_db.get(self.plugin_name).json() 
        if 'error' in template_dict:
            template_dict = {}
        else: 
            template_dict = {self.ast.literal_eval(k) : v for k, v in template_dict.items()
                             if not k.startswith('_')}
        return template_dict

    def save_template_dict(self, templated_dict):
        if templated_dict:
            doc = self.crawler_template_db.get(self.plugin_name).json()
            if 'error' in doc:
                doc = {}
            doc.update({repr(k) : v for k, v in templated_dict.items()}) 
            self.crawler_template_db[self.plugin_name] = doc
