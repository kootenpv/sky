import os
import json
import shutil
from sky.helper import slugify


class BareCache():

    def __init__(self, server=None, load_on_init=True, flush_cache=False):
        self.project_name = None
        self.plugin_name = None
        self.load_on_init = load_on_init
        self.flush_cache = flush_cache
        self.server = server
        self.dict = {}

    def setup(self):
        if self.server is None:
            raise ValueError("No server object given; it is unclear where to store data.")

        if self.flush_cache:
            self.delete_cache()

        self.load_index()

        if not self.flush_cache and self.load_on_init:
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
        This will load all the available slugified URLs, so it is known which html data is available
        """
        raise NotImplementedError("'load_index' is not implemented for Cache")

    def load_all(self):
        """
        This will load the html_data for all known slugified URLs
        """
        raise NotImplementedError("'load_all' is not implemented for Cache")


class FileCache(BareCache):

    def load_index(self):
        cache_data = {}
        for fn in os.listdir(self.server['cache']):
            slugged_plugin = slugify(self.plugin_name)
            for fn in os.listdir(self.server['cache']):
                if slugged_plugin in fn:
                    cache_data[fn] = False
        self.dict = cache_data

    def load_all(self):
        for fn in self.dict:
            self.load_page_from_cache(fn)

    def load_page_from_cache(self, fn):
        with open(os.path.join(self.server['cache'], fn)) as f:
            response_data = json.load(f)
        return response_data['html']

    def delete_cache(self):
        shutil.rmtree(self.server['cache'])

    def __getitem__(self, x):
        if not self.dict[x]:
            self.dict[x] = self.load_page_from_cache(x)
        return self.dict[x]

    def __setitem__(self, key, item):
        with open(os.path.join(self.server['cache'], key)) as f:
            json.dump(item, f)
        self.dict[key] = item

    def __contains__(self, key):
        return key in self.dict
