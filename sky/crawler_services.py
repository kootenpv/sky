import os
import json

from sky.helper import slugify

try:
    from ZODB.serialize import referencesf
    from ZODB.DB import DB
    import transaction
    from BTrees.OOBTree import OOBTree
    import time
except ImportError:
    msg = 'ZODB not properly installed and cannot be used as data backend.\n'
    msg += 'Use `pip3 install ZODB zodbpickle` to install, or use a different backend.'
    print(msg)


class CrawlService():

    def __init__(self, project_name, storage_object, crawl_plugin_class, cache=None):
        self.project_name = project_name
        self.storage_object = storage_object
        self.cache = cache
        self.plugin_configs = {}
        self.server = None
        self.crawl_plugin_class = crawl_plugin_class
        self.get_server()
        self.get_crawl_plugins()

    def __getitem__(self, plugin_name):
        if not isinstance(plugin_name, str):
            m = "To subset CrawlService, a string referring to the CrawlPlugin has to be provided"
            raise TypeError(m)
        return self.get_crawl_plugin(plugin_name)

    def get_server(self):
        raise NotImplementedError("get_server not implemented")

    def get_crawl_plugins(self):
        raise NotImplementedError("get_crawl_plugins not implemented")

    def get_documents(self):
        raise NotImplementedError("get_documents not implemented")

    def get_crawl_plugin(self, plugin_name):
        return self.crawl_plugin_class(self.project_name, self.server, plugin_name, self.cache)

    def run(self, plugin_name, delete_existing_documents=False):
        cplug = self.get_crawl_plugin(plugin_name)
        cplug.run(delete_existing_documents)

    def run_all(self, delete_existing_documents=False):
        for plugin in self.plugin_configs:
            self.run(plugin, delete_existing_documents)


class CrawlFileService(CrawlService):

    def get_server(self):
        root = self.storage_object['path']
        tps = ['plugins', 'documents', 'template_dict']
        self.server = {tp: os.path.join(root, self.project_name + '-crawler-' + tp)
                       for tp in tps}
        # create paths if they don't exist
        for paths in self.server.values():
            os.makedirs(paths, exist_ok=True)

    def get_crawl_plugins(self):
        self.plugin_configs = {}
        for fn in os.listdir(self.server['plugins']):
            if fn != 'default':
                with open(os.path.join(self.server['plugins'], fn)) as f:
                    # not yet parsed config, not sure if that is a problem
                    self.plugin_configs[fn] = f.read()

    def get_documents(self):
        documents = {}
        for fn in os.listdir(self.server['documents']):
            with open(os.path.join(self.server['plugins'], fn)) as f:
                # not yet parsed config, not sure if that is a problem
                documents[fn] = json.load(f)


class CrawlCloudantService(CrawlService):

    def delete_doc_id(self, doc_id):
        doc = self.server[self.project_name + '-crawler-documents'].document(doc_id)
        rev = doc.get().result().json()['_rev']
        return doc.delete(rev)

    def delete_doc(self, doc_id, doc_rev):
        doc = self.server[self.project_name + '-crawler-documents'].document(doc_id)
        return doc.delete(doc_rev)

    def delete_doc_url(self, url=None):
        return self.delete_doc_id(slugify(url))

    def get_server(self):
        account = self.storage_object

        # create dbs if they don't exist
        account.database(self.project_name + '-crawler-plugins').put()
        account.database(self.project_name + '-crawler-documents').put()
        account.database(self.project_name + '-crawler-template_dict').put()

        self.add_url_view()

        self.server = account

    def add_url_view(self):
        url_view_design = {
            "views": {
                "view1": {
                    "map": "function(doc){emit(doc.url)}"
                }
            }
        }
        doc_db = self.storage_object.database(self.project_name + '-crawler-documents')
        if doc_db['_design/urlview'].head().result().status_code != 200:
            doc_db['_design/urlview'] = url_view_design

    def get_crawl_plugins(self):
        plugin_db = self.server.database(self.project_name + '-crawler-plugins')
        db_uri = '{}/_all_docs?include_docs=true'.format(plugin_db.uri)
        service_rows = plugin_db.get(db_uri).result().json()['rows']
        self.plugin_configs = {row['doc']['_id']: row['doc'] for row in service_rows
                               if 'default' != row['doc']['_id']}

    def get_documents(self):
        document_db = self.server.database(self.project_name + '-crawler-documents')
        db_uri = '{}/_all_docs?include_docs=true'.format(document_db.uri)
        service_rows = document_db.get(db_uri).result().json()['rows']
        return {row['doc']['_id']: row['doc'] for row in service_rows
                if not row['doc']['_id'].startswith('_')}


class CrawlZODBService(CrawlService):

    def get_server(self):
        # In services, a FileStorage (or perhaps other backend) object has to be provided
        db = DB(self.storage_object)
        connection = db.open()
        self.server = connection.root()

        # create dbs if they don't exist
        tables = ['plugins', 'documents', 'template-dict']
        for table in tables:
            if table not in self.server:
                self.server[table] = OOBTree()
                transaction.commit()

    def pack(self):
        self.storage_object.pack(time.time(), referencesf)

    def get_crawl_plugins(self):
        return {k: doc for k, doc in self.server['plugins'].items() if k != 'default'}

    def get_documents(self):
        return {k: doc for k, doc in self.server['documents'].items()}


class CrawlElasticSearchService(CrawlService):

    def create_index_if_not_existent(self, name, request_body=None):
        if not self.server.indices.exists(name):
            if request_body is None:
                request_body = {
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0
                    }
                }
            self.server.indices.create(index=name, body=request_body)

    def get_server(self):
        self.server = self.storage_object

        # create dbs if they don't exist
        for db in ['plugins', 'documents', 'template_dict']:
            self.create_index_if_not_existent(self.project_name + '-crawler-' + db)

    def get_crawl_plugins(self):
        query = {"query": {"match_all": {}}}
        res = self.server.search(body=query, doc_type='plugin',
                                 index=self.project_name + "-crawler-plugins")
        return {doc['_id']: doc for doc in res['hits']['hits']
                if doc['_id'] != 'default'}

    def get_documents(self):
        query = {"query": {"match_all": {}}}
        res = self.server.search(body=query, doc_type='document',
                                 index=self.project_name + "-crawler-documents")
        return {doc['_id']: doc for doc in res['hits']['hits']}
