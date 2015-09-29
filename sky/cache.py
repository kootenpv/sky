import os
import json
import shutil
from sky.helper import slugify


class BareCache():

    def __init__(self, storage_object=None, load_on_init=True, flush_cache=False,
                 only_save_index_pages=True):
        self.project_name = None
        self.only_save_index_pages = only_save_index_pages
        self.plugin_name = None
        self.load_on_init = load_on_init
        self.flush_cache = flush_cache
        self.server = None
        self.storage_object = storage_object
        self.dict = {}
        self.prefix = None

    def init_cache_storage(self):
        raise NotImplementedError('init_cache_storage is not implemented for Cache')

    def setup(self):
        if self.storage_object is None:
            raise ValueError("No storage_object given; it is unclear where to store data.")

        self.init_cache_storage()

        print("loading cache index")
        self.load_index()

        if not self.flush_cache and self.load_on_init:
            print("loading whole cache")
            self.load_all()

    def delete_cache(self):
        raise NotImplementedError("'delete_cache' is not implemented for Cache")

    def __getitem__(self, key):
        raise NotImplementedError("'__getitem__' is not implemented for Cache", key)

    def __setitem__(self, key, item):
        raise NotImplementedError("'__setitem__' is not implemented for Cache", key, item)

    def __contains__(self, key):
        raise NotImplementedError("'__contains__' is not implemented for Cache", key)

    def load_index(self):
        """
        This will load all the available slugified URLs, so it is known which data is available
        """
        raise NotImplementedError("'load_index' is not implemented for Cache")

    def load_all(self):
        """
        This will load the data for all known slugified URLs
        """
        raise NotImplementedError("'load_all' is not implemented for Cache")


class FileCache(BareCache):

    def init_cache_storage(self):
        root = self.storage_object['path']

        self.prefix = slugify(self.plugin_name)

        self.server = {'cache':
                       os.path.join(root, self.project_name + '-crawler-cache', self.prefix)}

        if self.flush_cache:
            self.delete_cache()

        for paths in self.server.values():
            os.makedirs(paths, exist_ok=True)

    def load_index(self):
        cache_data = {}
        for fn in os.listdir(self.server['cache']):
            for fn in os.listdir(os.path.join(self.server['cache'])):
                cache_data[fn] = False
        self.dict = cache_data

    def load_all(self):
        for fn in self.dict:
            self.load_page_from_cache(fn)

    def load_page_from_cache(self, fn):
        full_path = os.path.join(self.server['cache'], fn)
        if not os.path.isfile(full_path):
            return False

        with open(full_path) as f:
            response_data = json.load(f)
        return response_data

    def delete_cache(self):
        shutil.rmtree(self.server['cache'])

    def __getitem__(self, x):
        if not self.dict[x]:
            self.dict[x] = self.load_page_from_cache(x)
        return self.dict[x]

    def __setitem__(self, key, item):
        with open(os.path.join(self.server['cache'], key), 'w') as f:
            json.dump(item, f)
        self.dict[key] = item

    def __contains__(self, key):
        return key in self.dict


# class CloudantCache(BareCache):

#     def init_cache_storage(self):

#         self.server = {'cache': self.storage_object.database(self.project_name + '-crawler-cache')}

#         if self.flush_cache:
#             self.delete_cache()

#         # create db if it doesn't exist
#         self.server['cache'].put()

#     def load_index(self):
#         cache_data = {}
#         for fn in os.listdir(self.server['cache']):
#             slugged_plugin = slugify(self.plugin_name)
#             for fn in os.listdir(self.server['cache']):
#                 if slugged_plugin in fn:
#                     cache_data[fn] = False
#         self.dict = cache_data

#     def load_all(self):
#         for fn in self.dict:
#             self.load_page_from_cache(fn)

#     def load_page_from_cache(self, fn):
#         full_path = os.path.join(self.server['cache'], fn)
#         if not os.path.isfile(full_path):
#             return False

#         with open(full_path) as f:
#             response_data = json.load(f)
#         return response_data

#     def delete_cache(self):
#         shutil.rmtree(self.server['cache'])

#     def __getitem__(self, x):
#         if not self.dict[x]:
#             self.dict[x] = self.load_page_from_cache(x)
#         return self.dict[x]

#     def __setitem__(self, key, item):
#         with open(os.path.join(self.server['cache'], key), 'w') as f:
#             json.dump(item, f)
#         self.dict[key] = item

#     def __contains__(self, key):
#         return key in self.dict
