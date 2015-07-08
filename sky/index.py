import os
import json
import lxml.html
import langdetect

try: 
    from .helper import *
    from .templated import DomainNodesDict
    from .findTitle import getRuleTitle, getTitle
    from .get_date import get_dates
except SystemError: 
    from helper import *
    from findTitle import getRuleTitle, getTitle
    from templated import DomainNodesDict
    from get_date import get_dates

def get_language(tree, headers):
    lang = None
    
    if headers and 'content-language' in headers:
        lang = headers['content-language']

    if lang is None and 'lang' in tree.attrib:
        lang = tree.attrib['lang']

    if lang is None:
        lang = langdetect.detect(lxml.html.tostring(tree).decode('utf8'))

    return lang or 'en'
        
class Index():
    def __init__(self, config): 
        self.config = config
        self.detected_language = None
        self.seed_urls = None 
        self.domain = None
        self.collections_path  = None
        self.collection_name = None 
        self.applyConfigFile() 
        self.domain = extractDomain(self.seed_urls[0])
        self.url_to_tree_mapping  = {}
        self.url_to_headers_mapping = {}
        self.load_pages()
        self.min_templates = None
        self.max_templates = None
        self.template_proportion = None
        self.domain_nodes_dict = DomainNodesDict(self.domain, self.min_templates, self.max_templates, self.template_proportion) 
        self.add_template_elements()

    def applyConfigFile(self):
        for config_key, config_value in self.config.items():
            setattr(self, config_key, config_value)
        self.domain = extractDomain(self.seed_urls[0])
        
    def load_pages(self): 
        saved_html_dir = os.path.join(self.collections_path, self.collection_name)
        for root, _, files in os.walk(saved_html_dir):
            for name in files:
                if '.DS_STORE' not in name:
                    with open(os.path.join(saved_html_dir, name)) as f:
                        js = json.load(f)
                        try:
                            self.url_to_tree_mapping[js['url']] = makeTree(js['html'], self.domain)
                            self.url_to_headers_mapping[js['url']] = js['headers']
                        except Exception as e:
                            print(str(e))
                        
    def add_template_elements(self): 
        for url in self.url_to_tree_mapping:
            self.domain_nodes_dict.add_template_elements(self.url_to_tree_mapping[url])

    def process(self, url, remove_visuals): 
        tree = self.url_to_tree_mapping[url]
        if self.detected_language is None:
            self.detected_language = get_language(tree, self.url_to_headers_mapping[url])
        pre_text_content = normalize('\n'.join([get_text_and_tail(x) for x in tree.iter()]))
        self.domain_nodes_dict.remove_template(tree)
        title = getRuleTitle(tree) 
        ok_imgs = get_images(tree)
        titleind = ()
        imginds = []
        contentinds = []

        # such as title, date and later author
        date_txt = []
        
        for num, node in enumerate(tree.iter()):
            if node.tag == 'img' and node in ok_imgs:
                imginds.append((node, num))
            elif normalize(get_text_and_tail(node)) == title:
                titleind = (node, num)
            elif get_text_and_tail(node).strip():
                contentinds.append((node, num))
            # Cleanup trash for visual'
            if remove_visuals:
                if node.tag == 'input':
                    node.set('type', 'hidden')
                elif node.tag == 'a' and not get_text_and_tail(node).strip():
                    for att in node.attrib:
                        node.set(att, '')
                if node.attrib and 'background-image' in node.attrib:
                    node.set('background-image', '')
        if titleind:
            sortedimgs = sorted(imginds, key = lambda x: abs(x[1] - titleind[1]))
        else:
            sortedimgs = []

        hardest_dates, fuzzy_hardest_dates, not_hardest_dates, soft_dates = get_dates(tree, self.detected_language)

        date = ''
        if titleind:
            if hardest_dates:
                print(hardest_dates)
                date = sorted(hardest_dates, key = lambda x: abs(x[1] - titleind[1]))[0][0]
            elif fuzzy_hardest_dates:
                date = sorted(fuzzy_hardest_dates, key = lambda x: abs(x[1] - titleind[1]))[0][0]
            elif not_hardest_dates:
                date = sorted(not_hardest_dates, key = lambda x: abs(x[1] - titleind[1]))[0][0]
        if not date and soft_dates:    
            for sd in soft_dates:
                date = sd
                break 

        # nu nog datum toevoegen, ook een prior voor in de buurt van titel
        body_content = []
        title_len = len(title)
        for x in tree.iter():
            txt = normalize(get_text_and_tail(x))
            if txt:
                n = len(txt)
                if n < title_len * 3 and title in txt:
                    continue
                body_content.append(txt)
                
                
        post_text_content = '\n'.join(body_content)
        
        print({'body' : post_text_content})
        print(len(pre_text_content) /len(post_text_content), url)
        return {'title' : title, 'body' : post_text_content, 'images' : sortedimgs, 'publish_date' : date, 'cleaned' : lxml.html.tostring(tree).decode('utf8') }

    def process_all(self, remove_visuals = False):
        results = {}
        for url in self.url_to_tree_mapping:
            results[url] = self.process(url, remove_visuals)
        return results    
        


from configs import DEFAULT_CRAWL_CONFIG
from helper import *

INDEX_CONFIG = DEFAULT_CRAWL_CONFIG.copy()

INDEX_CONFIG.update({ 
    'collections_path' : '/Users/pascal/GDrive/siteview/collections/',
    'seed_urls' : ['http://bankinnovation.net'],
    'collection_name' : 'bankinnovation.net',
    'template_proportion' : 0.09,
    'max_templates' : 1000
})

ind = Index(INDEX_CONFIG)
r = ind.process_all()

for k in r:
    break

    



# import json

# with open('/Users/pascal/GDrive/scrapy/fintech/bankinnovation_items.jsonlist') as f:
#     z = f.read().split('\n')

# urls = []
# htmls = []
# for x in z:
#     urls.append(json.loads(x)['url'])
#     htmls.append(json.loads(x)['body'])

# newurls = []
# newhtmls = []    
# for url, html in zip(urls, htmls):
#     if url.count('/') == 6: 
#         if any([x in url for x in ['2013', '2014', '2015']]):
#             newurls.append(url)
#             newhtmls.append(html)
