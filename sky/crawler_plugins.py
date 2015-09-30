# grote issue: crawler_plugin save_config does not remove old values


# ccp.dbs['documents'].document(x['_id']).delete(x['_rev'])


# split into separate files for DBs, or should I?

# Take care of backend for handle results
# for new project
# Create the databases
# Create the "default" document in plugins
# Create the design document

import json
import os

from sky.scraper import Scraper
from sky.crawler import crawl
from sky.crawler.crawling import NewsCrawler
from sky.helper import slugify
from sky.helper import chunker

import requests

# ZODB specific
try:
    import transaction
    from BTrees.OOBTree import OOBTree
except ImportError:
    print('Optional ZODB not possible as backend. Use `pip3 install ZODB zodbpickle`')


class CrawlPlugin:

    def __init__(self, project_name, server=None, plugin_name=None, cache=None):
        self.project_name = project_name
        self.plugin_name = plugin_name
        self.server = server
        self.cache = self.prepare_cache(cache)
        self.crawl_config = None
        self.data = {}
        self.documents = []
        self.template_dict = None

    def prepare_cache(self, cache):
        if cache is not None:
            cache.plugin_name = self.plugin_name
            cache.project_name = self.project_name
            cache.setup()
        return cache

    def get_default_plugin(self):
        pass

    def get_specific_plugin(self):
        pass

    def start_crawl(self):
        crawl.start(self.crawl_config, cache=self.cache)

    def scrape_data(self):
        # Create boilerplate recognizer
        skindex = Scraper(self.crawl_config)

        skindex.load_local_pages()
        skindex.add_template_elements()

        # Process all by removing boilerplate and extracting information
        return skindex.process_all(exclude_data=['cleaned', 'author'])

    def get_documents(self, maximum_number_of_documents=10000):
        pass

    def save_bulk_data(self, data):
        pass

    def run(self, delete_existing_documents=False):
        # get default plugin
        self.crawl_config = self.get_default_plugin()
        self.start_crawl()
        self.data = self.scrape_data()
        self.save_bulk_data(self.data)

    def get_bad_summary(self, force_get_documents=False, n=5):
        if not self.documents or force_get_documents:
            self.documents = self.get_documents()
        title_sort = sorted(self.documents, key=lambda doc: len(doc['title']))
        body_sort = sorted(self.documents, key=lambda doc: len(' '.join(doc['body'])))
        date_sort = sorted(self.documents, key=lambda doc: len(doc['publish_date']))
        url_sort = sorted(self.documents, key=lambda doc: len(doc['url']))
        return {k: [(d['url'], d[k]) for d in sorted_type][:n]
                for k, sorted_type in zip(['title', 'body', 'publish_date', 'url'],
                                          [title_sort, body_sort, date_sort, url_sort])}


class CrawlFilePlugin(CrawlPlugin):

    def get_default_plugin(self):
        with open(os.path.join(self.server['plugins'], 'default')) as f:
            return json.load(f)

    def get_specific_plugin(self):
        with open(os.path.join(self.server['plugins'], self.plugin_name)) as f:
            specific_config = json.load(f)
        return specific_config

    def save_bulk_data(self, data):
        for row in data:
            with open(os.path.join(self.server['documents'], slugify(data[row]['url'])), 'w') as f:
                json.dump(data[row], f)

    def get_documents(self, maximum_number_of_documents=1000000):
        slugged_url = slugify(self.plugin_name)
        results = []
        for num, fn in enumerate(os.listdir(self.server['documents'])):
            if num == maximum_number_of_documents:
                break
            if slugged_url in fn:
                with open(os.path.join(self.server['documents'], fn)) as f:
                    results.append(json.load(f))
        return results

    def get_seen_urls(self):
        slugged_url = slugify(self.plugin_name)
        seen_urls = set()
        for fn in os.listdir(self.server['documents']):
            if slugged_url in fn:
                with open(os.path.join(self.server['documents'], fn)) as f:
                    seen_urls.add(json.load(f)['url'])
        return seen_urls

    def save_config(self, config):
        with open(os.path.join(self.server['plugins'], self.plugin_name), 'w') as f:
            json.dump(config, f)


class CrawlCloudantPlugin(CrawlPlugin):

    def __init__(self, project_name, server, plugin_name, cache):
        super(CrawlCloudantPlugin, self).__init__(project_name, server, plugin_name, cache)
        self.dbs = {x: self.server.database(self.project_name + '-crawler-' + x) for x in
                    ['plugins', 'documents', 'template_dict']}

    def get_default_plugin(self):
        return self.dbs['plugins'].get('default').result().json()

    def get_specific_plugin(self):
        return self.dbs['plugins'].get(self.plugin_name).result().json()

    def save_bulk_data(self, data):
        for url_id in data:
            data[url_id]['_id'] = slugify(url_id)
        # save bulk per max 10k per time
        for chunk in chunker(data.values(), 10000):
            if not chunk:
                return
            self.dbs['documents'].bulk_docs(*[x for x in chunk if x is not None]).result()

    def get_documents(self, maximum_number_of_documents=1000000):
        # now just to add the host thing ??????????????
        query = 'query={}'.format(self.plugin_name)
        params = '?include_docs=true&limit={}&{}'.format(maximum_number_of_documents, query)
        return [x['doc'] for x in self.dbs['documents'].all_docs().get(params).result().json()['rows']
                if 'url' in x['doc'] and self.plugin_name in x['doc']['url']]

    def delete_existing_documents(self):
        return [self.dbs['documents'].document(x['_id']).delete(x['_rev'])
                for x in self.get_documents()]

    def get_seen_urls(self):
        # params = '?query={}'.format(self.plugin_name) # werkt niet
        params = ''
        udocs = self.dbs['documents'].design('urlview').view('view1').get(params).result().json()
        if 'rows' in udocs:
            return set([udoc['key'] for udoc in udocs['rows'] if self.plugin_name in udoc['key']])
        else:
            print("no seen urls for plugin", self.plugin_name)
            return set()

    def save_config(self, config):
        doc = self.dbs['plugins'].get(self.plugin_name).result().json()
        if 'error' not in doc:
            config['_id'] = doc['_id']
            config['_rev'] = doc['_rev']
        self.dbs['plugins'][self.plugin_name] = config


class CrawlElasticSearchPlugin(CrawlPlugin):

    def __init__(self, project_name, server, plugin_name, cache):
        super(CrawlElasticSearchPlugin, self).__init__(project_name, server, plugin_name, cache)
        self.es = server

    def get_default_plugin(self):
        return self.es.get(id='default', doc_type='plugin',
                           index=self.project_name + "-crawler-plugins")['_source']

    def get_specific_plugin(self):
        return self.es.get(id=self.plugin_name, doc_type='plugin',
                           index=self.project_name + "-crawler-plugins")['_source']

    def save_bulk_data(self, data):
        for url_id in data:
            doc_id = slugify(url_id)
            self.es.index(id=doc_id, body=data[url_id], doc_type='document',
                          index=self.project_name + "-crawler-documents")

    def get_documents(self, maximum_number_of_documents=1000000):
        query = {"query": {"wildcard": {"url": "*{}*".format(self.plugin_name)}}}
        res = self.es.search(body=query, doc_type='document',
                             index=self.project_name + "-crawler-documents")
        return res['hits']['hits']

    def get_seen_urls(self):
        query = {"query": {"wildcard": {"url": "*{}*".format(self.plugin_name)}}, "fields": "url"}
        res = self.es.search(body=query, doc_type='document',
                             index=self.project_name + "-crawler-documents")
        return set([x['fields']['url'][0] for x in res['hits']['hits']])

    def save_config(self, config):
        self.es.index(id=self.plugin_name, body=config, doc_type='plugin',
                      index=self.project_name + "-crawler-plugins")


class CrawlZODBPlugin(CrawlPlugin):

    def get_default_plugin(self):
        return self.server['plugins']['default']

    def get_specific_plugin(self):
        return self.server['plugins'][self.plugin_name]

    def save_bulk_data(self, data):
        for url_id in data:
            self.server['documents'][slugify(url_id)] = data[url_id]
        transaction.commit()

    def get_documents(self, maximum_number_of_documents=1000000):
        return self.server['documents']

    def delete_existing_documents(self):
        self.server['documents'] = OOBTree()
        transaction.commit()

    def get_seen_urls(self):
        return set([self.server['documents'][s]['url'] for s in self.server['documents']
                    if self.plugin_name in self.server['documents'][s]['url']])

    def save_config(self, config):
        self.server['plugins'][self.plugin_name] = config
        transaction.commit()


class CrawlPluginNews(CrawlPlugin):
    import ast

    def save_data(self, data):
        raise NotImplementedError('save_data required')

    def get_template_dict(self):
        raise NotImplementedError('get_template_dict required')

    def save_template_dict(self, templated_dict):
        raise NotImplementedError('save_template_dict required')

    def get_seen_urls(self):
        raise NotImplementedError('seen_urls required')

    def delete_existing_documents(self):
        raise NotImplementedError('delete_existing_documents required')

    def run(self, delete_existing_documents=False):
        # get default plugin
        print("getting crawl plugin info")
        self.crawl_config = self.get_default_plugin()

        # apply this specific plugin
        self.crawl_config.update(self.get_specific_plugin())

        # delete existing documents
        if delete_existing_documents:
            print("deleting documents before crawling")
            self.delete_existing_documents()
            seen_urls = []
        # add the already visited urls to the config
        else:
            print("getting seen urls")
            seen_urls = self.get_seen_urls()
        self.crawl_config['seen_urls'] = seen_urls

        print("getting template dict")
        # add the template for this crawl_plugin to the scraping config
        self.crawl_config['template_dict'] = self.get_template_dict()

        print("starting crawl")
        # separate out the save data while crawling and the newscraler
        if 'logging_level' in self.crawl_config:
            logging_level = int(self.crawl_config['logging_level'])
        else:
            logging_level = 3
        templated_dict = crawl.start(
            self.crawl_config, NewsCrawler, self.save_data, self.save_bulk_data,
            logging_level=logging_level, cache=self.cache)

        print('saving template..')
        self.save_template_dict(templated_dict)
        print('crawling/scraping', self.project_name, self.plugin_name, "DONE")


class CrawlFilePluginNews(CrawlFilePlugin, CrawlPluginNews):

    def save_data(self, data):
        with open(os.path.join(self.server['documents'], slugify(data['url'])), 'w') as f:
            json.dump(data, f)

    def get_template_dict(self):
        temp_dict_fn = os.path.join(self.server['template_dict'], self.plugin_name)
        if os.path.isfile(temp_dict_fn):
            with open(temp_dict_fn) as f:
                template_dict = {self.ast.literal_eval(k): v for k, v in json.load(f).items()
                                 if not k.startswith('_')}
        else:
            template_dict = {}

        return template_dict

    def save_template_dict(self, templated_dict):
        if templated_dict:
            temp_dict_fn = os.path.join(self.server['template_dict'], self.plugin_name)
            with open(temp_dict_fn, 'w') as f:
                json.dump({repr(k): v for k, v in templated_dict.items()}, f)


class CrawlZODBPluginNews(CrawlZODBPlugin, CrawlPluginNews):

    def save_data(self, data):
        self.server['documents'][slugify(data['url'])] = data
        transaction.commit()

    def get_template_dict(self):
        if ('template_dict' not in self.server or
                self.plugin_name not in self.server['template_dict']):
            template_dict = OOBTree()
        else:
            template_dict = self.server['template_dict'][self.plugin_name]
        return template_dict

    def save_template_dict(self, templated_dict):
        if templated_dict:
            self.server['template_dict'][self.plugin_name] = OOBTree(templated_dict)
            transaction.commit()


class CrawlElasticSearchPluginNews(CrawlElasticSearchPlugin, CrawlPluginNews):

    def save_data(self, data):
        self.es.index(index=self.project_name + "-crawler-documents", doc_type='document',
                      id=slugify(data['url']), body=data)

    def get_template_dict(self):
        try:
            templ_dict = self.es.get(index=self.project_name + "-crawler-template_dict",
                                     doc_type='template_dict',
                                     id=self.plugin_name)['_source']
            templ_dict = {self.ast.literal_eval(k): v for k, v in templ_dict.items()}
        # In acually catching the NotFoundError (for which I do not want to depend
        # on importing the elasticsearch package)
        # pylint: disable=bare-except
        except:
            templ_dict = {}
        return templ_dict

    def save_template_dict(self, templ_dict):
        if templ_dict:
            try:
                self.es.index(index=self.project_name + "-crawler-template_dict",
                              doc_type='template_dict', id=self.plugin_name,
                              body=json.dumps({repr(k): v for k, v in templ_dict.items()}))
            # In acually catching the NotFoundError (for which I do not want to depend
            # on importing the elasticsearch package)
            # pylint: disable=bare-except
            except:
                self.es.update(
                    index=self.project_name + "-crawler-template_dict",
                    doc_type='template_dict', id=self.plugin_name,
                    body=json.dumps({"doc": {repr(k): v for k, v in templ_dict.items()}}))


class CrawlCloudantPluginNews(CrawlCloudantPlugin, CrawlPluginNews):

    def save_data(self, data):
        try:
            self.dbs['documents'][slugify(data['url'])] = data
        except requests.exceptions.HTTPError:
            print('conflict error', slugify(data['url']))

    def get_template_dict(self):
        template_dict = self.dbs['template_dict'].get(self.plugin_name).result().json()
        if 'error' in template_dict:
            template_dict = {}
        else:
            template_dict = {self.ast.literal_eval(k): v for k, v in template_dict.items()
                             if not k.startswith('_')}
        return template_dict

    def save_template_dict(self, templated_dict):
        if templated_dict:
            doc = self.dbs['template_dict'].get(self.plugin_name).result().json()
            if 'error' in doc:
                doc = {}
            doc.update({repr(k): v for k, v in templated_dict.items()})
            self.dbs['template_dict'][self.plugin_name] = doc
