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
    def __init__(self, project_name, server = None, plugin_name = None):
        self.project_name = project_name
        self.plugin_name = plugin_name 
        self.crawl_config = None
        self.scrape_config = None
        self.data = {}
        self.documents = []
        self.template_dict = None
        self.server = server

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
    def __init__(self, project_name, server, plugin_name): 
        super(CrawlCloudantPlugin, self).__init__(project_name, server, plugin_name) 
        self.dbs = {x : self.server.database(self.project_name + '-crawler-' + x) for x in 
                    ['plugins', 'documents', 'template_dict']}

    def get_default_plugin(self): 
        return self.dbs['plugins'].get('default').json()
        
    def apply_specific_plugin(self): 
        plugin = self.dbs['plugins'].get(self.plugin_name).json()
        self.crawl_config.update(plugin)
        seen_urls = self.get_seen_urls()
        self.crawl_config['seen_urls'] = seen_urls
        
    def handle_results(self, to = "cloudant"): 
        if to == "cloudant":
            for url_id in self.data: 
                self.data[url_id]['_id'] = slugify(url_id)
            self.dbs['documents'].bulk_docs(*list(self.data.values()))

    def get_documents(self, maximum_number_of_documents = 1000000): 
        # now just to add the host thing ??????????????
        query = 'query={}'.format(self.plugin_name)
        params = '?include_docs=true&limit={}&{}'.format(maximum_number_of_documents, query) 
        return [x['doc'] for x in self.dbs['documents'].all_docs().get(params).json()['rows']
                if self.plugin_name in x['doc']['url']]

    def get_seen_urls(self): 
        params = '?query={}'.format(self.plugin_name) 
        udocs = self.dbs['documents'].design('urlview').view('view1').get(params).json()['rows']
        return set([udoc['key'] for udoc in udocs])
        
    def save_config(self, config):
        doc = self.dbs['plugins'].get(self.plugin_name).json()
        if 'error' in doc:
            doc = {}
        doc.update(config) 
        self.dbs['plugins'][self.plugin_name] = doc

class CrawlElasticSearchPlugin(CrawlPlugin):
    ### 
    # Make it so that the service can do the login once, and that this receives the databases 
    ###
    ### Class import
    from elasticsearch import Elasticsearch
    import elasticsearch
    def __init__(self, project_name, server, plugin_name): 
        super(CrawlElasticSearchPlugin, self).__init__(project_name, server, plugin_name)
        self.es = server

    def get_default_plugin(self): 
        return self.es.get(id = 'default', doc_type = 'plugin', 
                           index = self.project_name + "-crawler-plugins")['_source']
        
    def apply_specific_plugin(self): 
        conf = self.es.get(id = self.plugin_name, doc_type = 'plugin', 
                           index = self.project_name + "-crawler-plugins")['_source']
        self.crawl_config.update(conf)        
        seen_urls = self.get_seen_urls()
        self.crawl_config['seen_urls'] = seen_urls
        
    def handle_results(self, to = "cloudant"): 
        for url_id in self.data: 
            doc_id = slugify(url_id) 
            self.es.index(id = doc_id, body = self.data[url_id], doc_type = 'document', 
                          index = self.project_name + "-crawler-documents")
        print(to)    

    def get_documents(self, maximum_number_of_documents = 1000000): 
        query = {"query": {"wildcard": {"url": "*{}*".format(self.plugin_name)}}}
        res = self.es.search(body = query, doc_type = 'document', 
                             index = self.project_name + "-crawler-documents")
        return res['hits']['hits']

    def get_seen_urls(self): 
        query = {"query": {"wildcard": {"url": "*{}*".format(self.plugin_name)}}, "fields" : "url"}        
        res = self.es.search(body = query, doc_type = 'document', 
                             index = self.project_name + "-crawler-documents")
        return set([x['fields']['url'][0] for x in res['hits']['hits']])
        
    def save_config(self, config):
        self.es.index(id = self.plugin_name, body = config, doc_type = 'plugin', 
                      index = self.project_name + "-crawler-plugins")

class CrawlZODBPlugin(CrawlPlugin):
    import transaction
    from BTrees.OOBTree import OOBTree
    
    def __init__(self, project_name, server, plugin_name): 
        super(CrawlZODBPlugin, self).__init__(project_name, server, plugin_name) 

    def get_default_plugin(self): 
        return self.server['plugins']['default']
        
    def apply_specific_plugin(self): 
        conf = self.server['plugins'][self.plugin_name]
        self.crawl_config.update(conf)        
        seen_urls = self.get_seen_urls()
        self.crawl_config['seen_urls'] = seen_urls
        
    def handle_results(self, to = "cloudant"): 
        for url_id in self.data: 
            self.server['documents'][slugify(url_id)] = self.data[url_id]
        self.transaction.commit()
        print(to)    

    def get_documents(self, maximum_number_of_documents = 1000000): 
        return self.server['documents']

    def get_seen_urls(self): 
        return set([self.server['documents'][s]['url'] for s in self.server['documents'] 
                    if self.plugin_name in self.server['documents'][s]['url']]) 
        
    def save_config(self, config):
        self.server['plugins'][self.plugin_name] = config
        self.transaction.commit()

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
        self.server['documents'][slugify(data['url'])] = data
        self.transaction.commit()

    def get_template_dict(self):
        if ('template-dict' not in self.server or
            self.plugin_name not in self.server['template-dict']): 
            template_dict = self.OOBTree()
        else:
            template_dict = self.server['template-dict'][self.plugin_name]
        return template_dict

    def save_template_dict(self, templated_dict):
        if templated_dict:
            self.server['template-dict'][self.plugin_name] = self.OOBTree(templated_dict)
            self.transaction.commit()

class CrawlElasticSearchPluginNews(CrawlElasticSearchPlugin, CrawlPluginNews): 

    def save_data_while_crawling(self, data): 
        self.es.index(index = self.project_name + "-crawler-documents", doc_type = 'document', 
                      id = slugify(data['url']), body = data) 

    def get_template_dict(self):
        try:
            template_dict = self.es.get(index = self.project_name + "-crawler-template-dict", 
                                        doc_type = 'template-dict', 
                                        id = self.plugin_name)['_source']
            template_dict = {self.ast.literal_eval(k) : v for k,v in template_dict.items()}
        except self.elasticsearch.NotFoundError:
            template_dict = {}
        return template_dict

    def save_template_dict(self, templated_dict):
        if templated_dict:
            try:
                self.es.index(index = self.project_name + "-crawler-template-dict", doc_type = 'template-dict', id = self.plugin_name, 
                               body = json.dumps({repr(k): v for k, v in templated_dict.items()}))
            except self.elasticsearch.RequestError: 
                self.es.update(index = self.project_name + "-crawler-template-dict", doc_type = 'template-dict', id = self.plugin_name, 
                               body = json.dumps({"doc" : {repr(k): v for k, v in templated_dict.items()}}))

class CrawlCloudantPluginNews(CrawlCloudantPlugin, CrawlPluginNews): 

    def save_data_while_crawling(self, data): 
        self.dbs['documents'][slugify(data['url'])] = data

    def get_template_dict(self): 
        template_dict = self.dbs['template-dict'].get(self.plugin_name).json() 
        if 'error' in template_dict:
            template_dict = {}
        else: 
            template_dict = {self.ast.literal_eval(k) : v for k, v in template_dict.items()
                             if not k.startswith('_')}
        return template_dict

    def save_template_dict(self, templated_dict):
        if templated_dict:
            doc = self.dbs['template-dict'].get(self.plugin_name).json()
            if 'error' in doc:
                doc = {}
            doc.update({repr(k) : v for k, v in templated_dict.items()}) 
            self.dbs['template-dict'][self.plugin_name] = doc
