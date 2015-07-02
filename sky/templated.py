try: 
    from .helper import * 
    from .findTitle import getTitle
except SystemError: 
    from helper import *
    from findTitle import getTitle

class DomainNodesDict(dict):
    def __init__(self, domain):
        super(DomainNodesDict, self).__init__()
        self.num_urls = 0 
        self.domain = domain

    def get_fingerprints(self, node):
        res = []
        text = get_text_and_tail(node).strip() 
        if text: 
            res = [(node.tag, a, node.attrib[a], text) for a in node.attrib] 
            if not res:
                res = [(node.tag, '', '', text)]
        return res
        
    def add_template_elements(self, tree):
        seen = set()
        for node in tree.iter():
            for fp in self.get_fingerprints(node):
                if fp not in self:
                    self[fp] = 0
                if fp not in seen:    
                    self[fp] += 1
                    seen.add(fp)
        self.num_urls += 1
        
    def remove_template(self, tree, min_templates = 2):
        if min_templates < self.num_urls:
            raise ValueError('Not enough urls')
        for node in tree.iter():
            for fp in self.get_fingerprints(node):
                if fp in self and self[fp] / self.num_urls > 0.9: 
                    node.text = ''
                    node.tail = ''

class DomainImagesDict(dict):
    def __init__(self, domain, wrong_imgs = None):
        super(DomainImagesDict, self).__init__()
        self.num_urls = 0 
        self.domain = domain
        if wrong_imgs is None:
            self.wrong_imgs = ['icon', 'logo', 'advert', 'toolbar', 'footer', 'layout', 'banner'] 
        else:
            self.wrong_imgs = wrong_imgs
            
    def get_images(self, tree): 
        img_links = list(set([x for x in tree.xpath('//meta[contains(@property, "image")]/@content') 
                              if not any([w in x for w in self.wrong_imgs])])) 
        img_links += list(set([x for x in tree.xpath('//img/@src') if not any([w in x for w in self.wrong_imgs])])) 
        img_links = [x for x in img_links if x.startswith('http')]
        return img_links

    def add_template_elements(self, tree):
        for img in set(self.get_images(tree)):
            if img not in self:
                self[img] = 0
            self[img] += 1
        self.num_urls += 1    
        
    def remove_template(self, tree, min_templates = 2):
        if min_templates > self.num_urls:
            raise ValueError('Not enough urls') 
        for meta_content in tree.xpath('//meta[contains(@property, "image") and @content]'):
            meta_img = meta_content.attrib['content']
            if meta_img in self and self[meta_img] / self.num_urls > 0.9: 
                meta_content.set('content', '')
        for img in tree.xpath('//img[@src]'):
            img_src = img.attrib['src']
            if img_src in self and self[img_src] / self.num_urls > 0.9: 
                img.set('src', '')                    
                        
u1 = 'http://www.nieuwsdumper.nl/nieuws/1454/eerste-volvo-fmx-410-8x4-tridem-betonmixer-voor-bck.html'
u2 = 'http://www.nieuwsdumper.nl/nieuws/1680/volvo-fh-500-8x2-voor-aannemersbedrijf-h-mulder-b-v-.html'
                        
tu1 = getQuickTree(u1)
tu2 = getQuickTree(u2)

a = DomainNodesDict('http://www.nieuwsdumper.nl/')
a.add_template_elements(tu1)
a.add_template_elements(tu2)

b = DomainImagesDict('http://www.nieuwsdumper.nl/')
b.add_template_elements(tu1)
b.add_template_elements(tu2)


bla = tu2.text_content()
a.remove_template(tu2)
bla2 = tu2.text_content()


for i in tu2.iter():
    if i.tag == 'img' and 'src' in i.attrib and i.attrib['src']:
        print(i.tag)
    print(get_text_and_tail(i))



    
