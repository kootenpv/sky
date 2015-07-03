import os
import json

try: 
    from .helper import *
    from .templated import DomainNodesDict
    from .findTitle import getRuleTitle
except SystemError: 
    from helper import *
    from findTitle import getRuleTitle
    from templated import DomainNodesDict

class Index():
    def __init__(self, config_filename): 
        self.config_filename = config_filename
        self.seed_urls = None
        self.domain = None
        self.collection_path  = None
        self.collection_name = None 
        self.applyConfigFile()
        self.domain = extractDomain(self.seed_urls[0])
        self.domain_nodes_dict = DomainNodesDict(self.domain) 
        self.url_to_tree_mapping  = {}
        self.add_template_elements()

    def applyConfigFile(self):
        with open(config_filename) as f:
            config = json.load(f)
        for config_key, config_value in config.items():
            setattr(self, config_key, config_value)
        
    def load_pages(self): 
        saved_html_dir = self.collection_path + self.collection_name
        for root, _, files in os.walk(saved_html_dir):
            for name in files:
                if '.DS_STORE' not in name:
                    with open(root + '/' + name) as f:
                        js = json.load(f)
                        try:
                            self.url_to_tree_mapping[js['url']] = makeTree(js['html'], self.domain)
                        except Exception as e:
                            print(str(e))
                        
    def add_template_elements(self): 
        for url in self.url_to_tree_mapping:
            self.domain_nodes_dict.add_template_elements(self.url_to_tree_mapping[url])

    def process(self, url):
        tree = self.url_to_tree_mapping[url]
        title = getRuleTitle(tree)
        ok_imgs = get_images(tree)
        titleind = ()
        imginds = []
        contentinds = []
        for num, node in enumerate(tree.iter()):
            if node.tag == 'img' and node in ok_imgs:
                imginds.append((node, num))
            elif normalize(get_text_and_tail(node)) == title:
                titleind = (node, num)
            elif get_text_and_tail(node).strip():
                contentinds.append((node, num))

        if titleind:
            sortedimgs = sorted(imginds, key = lambda x: abs(x[1] - titleind[1]))
        else:
            sortedimgs = []

        return {'title' : title, 'body' : tree.text_content, 'images' : sortedimgs}
