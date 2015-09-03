import re

from sky.helper import normalize
from sky.helper import get_text_and_tail


class DomainNodesDict(dict):

    def __init__(self, domain, min_templates=None, max_templates=None, template_proportion=None):
        super(DomainNodesDict, self).__init__()
        self.num_urls = 0
        self.domain = domain
        self.min_templates = min_templates or 2
        self.max_templates = max_templates or 24
        self.template_proportion = template_proportion or 0.7
        self.untemplated = []

    def get_fingerprints(self, node):
        res = []
        text = normalize(get_text_and_tail(node)).strip()
        if node.tag == 'a' and 'href' in node.attrib:
            res = [(node.tag, node.attrib['href'], '', '')]
        if text:
            res += [(node.tag, a, node.attrib[a], text) for a in node.attrib]
            if node.tag == 'a':
                res += [(node.tag, '', '', text)]
            if not res:
                res = [(node.tag, '', '', text)]
        else:
            if 'style' in node.attrib:
                tmp = re.findall(r'background-image:[ ]*url\((http[^)]+)', node.attrib['style'])
                if tmp:
                    res += [('style', tmp[0])]
        return res

    def add_fp(self, fp, seen):
        if fp not in seen:
            if fp not in self:
                self[fp] = 0
            self[fp] += 1
            seen.add(fp)

    def add_template_elements(self, tree):
        if self.num_urls < self.max_templates:
            seen = set()
            for node in tree.iter():
                if (node.tag == 'meta' and 'property' in node.attrib and
                        'image' in node.attrib['property'] and 'content' in node.attrib):
                    self.add_fp((node.attrib['property'], node.attrib['content']), seen)
                elif node.tag in ['img', 'iframe'] and 'src' in node.attrib:
                    self.add_fp((node.tag, node.attrib['src']), seen)
                else:
                    for fp in self.get_fingerprints(node):
                        self.add_fp(fp, seen)
            self.num_urls += 1

    def possible_author(self, node):
        goods = ['author', 'by', 'publi', 'write', 'written', 'info']
        attr_values = node.attrib.values()
        if any([g in a for a in attr_values for g in goods]):
            return True
        txt = get_text_and_tail(node)
        if re.search(r'\b(author|by)[: ]', txt):
            return True
        return False

    def remove_template(self, tree):
        if self.num_urls < self.min_templates:
            return False
        for node in tree.iter():
            if self.possible_author(node):
                continue
            if node.tag == 'meta':
                if 'property' in node.attrib and 'content' in node.attrib:
                    fp = (node.attrib['property'], node.attrib['content'])
                    if fp in self and self[fp] / self.num_urls > self.template_proportion:
                        node.set('content', '')
            elif node.tag in ['img', 'iframe'] and 'src' in node.attrib:
                fp = (node.tag, node.attrib['src'])
                if fp in self and self[fp] / self.num_urls > self.template_proportion:
                    node.set('src', '')
                    node.set('alt', '')
            else:
                for fp in self.get_fingerprints(node):
                    if fp in self and self[fp] / self.num_urls > self.template_proportion:
                        node.text = ''
                        node.tail = ''
                        if node.tag == 'a':
                            for child in node.iter():
                                child.text = ''
                                child.tail = ''

        return True

    def remove_author(self, tree):
        for node in tree.iter():
            if self.possible_author(node):
                if node.tag == 'meta':
                    if 'property' in node.attrib and 'content' in node.attrib:
                        fp = (node.attrib['property'], node.attrib['content'])
                        if fp in self and self[fp] / self.num_urls > self.template_proportion:
                            node.set('content', '')
                elif node.tag in ['img', 'iframe'] and 'src' in node.attrib:
                    fp = (node.tag, node.attrib['src'])
                    if fp in self and self[fp] / self.num_urls > self.template_proportion:
                        node.set('src', '')
                        node.set('alt', '')
                else:
                    for fp in self.get_fingerprints(node):
                        if fp in self and self[fp] / self.num_urls > self.template_proportion:
                            node.text = ''
                            node.tail = ''
                            if node.tag == 'a':
                                for child in node.iter():
                                    child.text = ''
                                    child.tail = ''
