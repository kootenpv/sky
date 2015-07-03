try: 
    from .helper import * 
    from .findTitle import getTitle
except SystemError: 
    from helper import *
    from findTitle import getTitle

class DomainNodesDict(dict):
    def __init__(self, domain, min_templates = 2, max_templates = 24):
        super(DomainNodesDict, self).__init__()
        self.num_urls = 0 
        self.domain = domain
        self.min_templates = min_templates
        self.max_templates = max_templates
        self.untemplated = []

    def get_fingerprints(self, node):
        res = []
        text = get_text_and_tail(node).strip() 
        if text: 
            res = [(node.tag, a, node.attrib[a], text) for a in node.attrib] 
            if not res:
                res = [(node.tag, '', '', text)]
        return res
        
    def add_template_elements(self, tree):
        if self.num_urls < self.max_templates:
            seen = set()
            for node in tree.iter():
                if node.tag == 'meta' and 'property' in node.attrib and 'image' in node.attrib['property'] and 'content' in node.attrib:
                    fp = (node.attrib['property'], node.attrib['content'])
                    if fp not in self:
                        self[fp] = 0
                    if fp not in seen:    
                        self[fp] += 1
                        seen.add(fp)
                elif node.tag == 'img' and 'src' in node.attrib:
                    fp = node.attrib['src']
                    if fp not in self:
                        self[fp] = 0
                    if fp not in seen:    
                        self[fp] += 1
                        seen.add(fp) 
                else:                        
                    for fp in self.get_fingerprints(node):
                        if fp not in self:
                            self[fp] = 0
                        if fp not in seen:    
                            self[fp] += 1
                            seen.add(fp)
            self.num_urls += 1

    def remove_template(self, tree):
        if self.num_urls < self.min_templates:
            return False
        for node in tree.iter():
            if node.tag == 'meta': 
                node.set('content', '')
                print('removed meta')
            elif node.tag == 'img':
                node.set('src', '')
                print('removed img')
            else:    
                for fp in self.get_fingerprints(node):
                    if fp in self and self[fp] / self.num_urls > 0.9: 
                            print('removed text')
                            node.text = ''
                            node.tail = ''
        return True

u1 = 'http://www.bbc.com/news/world-africa-33049312'
u2 = 'http://www.bbc.com/news/world-europe-33378778'
                        
tu1 = getQuickTree(u1)
tu2 = getQuickTree(u2)

a = DomainNodesDict('http://www.nieuwsdumper.nl/')
a.add_template_elements(tu1)
a.add_template_elements(tu2)

bla = tu2.text_content()

a.remove_template(tu2)

bla2 = tu2.text_content()

tit = getTitle(tu2)

for i in tu2.iter():
    if i.tag == 'img' and 'src' in i.attrib and i.attrib['src']:
        print(i.tag)
    if i.text == tit:
        print('titty')    
    print(get_text_and_tail(i))


    
# - similar pages templated removal
# - content nearness (img, publish)
# - known tags (img, title, publish)
# - difference over-time templated removal
# - not only remove duplicated     




- domain
- remove bad img tags
- add template tags
- check if page relevant when comparing template model
- get meta title things
- remove templates
- body
- title, based on text and meta
- publish
- images
- lang
- entities
