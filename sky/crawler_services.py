import os

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

    def __init__(self, project_name, storage_object, crawl_plugin_class):
        self.project_name = project_name
        self.storage_object = storage_object
        self.plugins = {}
        self.server = None
        self.crawl_plugin_class = crawl_plugin_class
        self.get_server()
        self.get_crawl_plugins()

    def get_server(self):
        raise NotImplementedError("get_server not implemented")

    def get_crawl_plugins(self):
        raise NotImplementedError("get_crawl_plugins not implemented")

    def get_crawl_plugin(self, plugin_name):
        return self.crawl_plugin_class(self.project_name, self.server, plugin_name)

    def run(self, plugin_name):
        cplug = self.get_crawl_plugin(plugin_name)
        cplug.run()

    def run_all(self):
        for plugin in self.plugins:
            self.run(plugin)


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
        self.plugins = {}
        for fn in os.listdir(self.server['plugins']):
            if fn != 'default':
                with open(os.path.join(self.server['plugins'], fn)) as f:
                    # not yet parsed config, not sure if that is a problem
                    self.plugins[fn] = f.read()


class CrawlCloudantService(CrawlService):

    def get_server(self):
        account = self.storage_object

        # create dbs if they don't exist
        account.database(self.project_name + '-crawler-plugins').put()
        account.database(self.project_name + '-crawler-documents').put()
        account.database(self.project_name + '-crawler-template_dict').put()

        self.server = account

    def get_crawl_plugins(self):
        plugin_db = self.server.database(self.project_name + '-crawler-plugins')
        db_uri = '{}/_all_docs?include_docs=true'.format(plugin_db.uri)
        service_rows = plugin_db.get(db_uri).result().json()['rows']
        self.plugins = {row['doc']['_id']: row['doc'] for row in service_rows
                        if 'default' != row['doc']['_id']}


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
