import lxml.html

try:
    from .training import Training
    from .helper import *
except SystemError:
    from training import Training    
    from helper import *

def metaPrinter(tr):
    for meta in tr.xpath('//meta'):
        print(lxml.html.tostring(meta))

def getNthInTree(tr, ele): 
    it = 0
    for x in tr.iter(): 
        it += 1
        if x == ele: 
            break
    else:
        return None
    return it

def getDepth(ele):
    return len(list(ele.iterancestors()))

def getTitle2(tree, returnBest = True):
    xpaths = ['//title', '//*[contains(@property, "title")]', '//*[contains(@name, "title")]', '//*[contains(@id, "title")]', '//*[@*="title"]', '//*[contains(@class, "title")]', '//*[@title]', '//h1', '//h2', '//h3', '//h4']
    titles = []
    for xp in xpaths:
        xres = tree.xpath(xp)
        if xres and len(xres[0].text_content().strip()) > 2:
            title = {}
            title['nthInTree'] = getNthInTree(tree, xres[0])
            title['depth'] = getDepth(xres[0])
            title['numElementsInXpath'] = len(xres)
            title['text'] = xres[0].text_content().strip()
            title['textLength'] = len(title['text'])
            title['isSub'] = False
            title['isSuper'] = False
            title['wordSet'] = set(x for x in title['text'].split() if len(x) > 1)
            title['wordSetLength'] = len(title['wordSet'])
            title['xpath'] = xp
            titles.append(title)
    scores = []
    for title in titles:
        scores.append(title['nthInTree'] * title['depth'] * title['numElementsInXpath']) 

    if not returnBest:
        return titles, scores
    
    for t, s in zip(titles, scores):
        if s == min(scores):
            for title, score in zip(titles, scores):
                
                if t != title:
                    if len(t['wordSet'] & title['wordSet']) / len(t['wordSet']) > 0.3 and t['wordSetLength'] > title['wordSetLength']:
                        break
            else:
                title, score = t, s
            return title, score        

def getTitle(tree, returnBest = True):
    xpaths = ['//title', '//*[contains(@name, "title")]', '//h1[contains(@id, "title")]', '//h1[contains(@class, "title")]', '//h1[@*="title"]', '//*[contains(@id, "title")]', '//*[@*="title"]', '//meta[contains(@property, "title")]', '//meta[contains(@property, "title")]/@content', '//*[contains(@class, "title")]', '//*[@title]', '//h1', '//h2', '//h3', '//h4', '//strong']
    # xpaths = ['//title', '//meta[contains(@property, "title")]', '//*[contains(@name, "title")]', '//h1[contains(@id, "title")]', '//h1[contains(@class, "title")]', '//h1[@*="title"]', '//*[contains(@id, "title")]', '//*[@*="title"]', '//*[contains(@class, "title")]', '//*[@title]', '//h1', '//h2', '//h3', '//h4']
    titles = []
    for xp in xpaths:
        xres = tree.xpath(xp)
        title = {}
        if xres: 
            if isinstance(xres[0], lxml.html.HtmlElement):
                title['text'] = xres[0].text_content().strip()
            else:
                title['text'] = xres[0]   
            if len(title['text']) < 3:
                continue
            title['wordSet'] = set(x for x in title['text'].split() if len(x) > 1)
            title['wordSetLength'] = len(title['wordSet'])
            title['xpath'] = xp
            titles.append(title)

    if not returnBest:
        return titles

    t = titles[0]
    for title in titles[1:]:
        if len(t['wordSet'] & title['wordSet']) / len(t['wordSet']) > 0.3 and t['wordSetLength'] > title['wordSetLength']: 
            break
    else:
        title = t
    return title['text']


# tr = Training("nieuwsdumper-testcase1", "/Users/pascal/GDrive/virtual-python/sky/sky/tests/").load()
# tr2 = Training("marktplaats-testcase1", "/Users/pascal/GDrive/virtual-python/sky/sky/tests/").load()
# tr3 = Training("betterdoctor-doctor-referalls", "/Users/pascal/GDrive/virtual-python/sky/sky/tests/").load()

    
# train = [tr, tr2, tr3]            
# for t in train:
#     for tree in t.trees:
#         print(getTitle(tree))
            










# TITLE TESTS









title = normalize(''.join([x for x in z.xpath('//span[@class="x-nc-sel1"]/text()')]))

body = normalize(''.join([x for x in z.xpath('//span[@class="x-nc-sel2"]/text()')]))

with open('/Users/pascal/Downloads/L3S-GN1-20100130203947-00001/url-mapping.txt') as f:
    urlmapping = {x[10:46] : [x[48:], extractDomain(x[48:])] for x in f.read().split('\n')}

template = '/Users/pascal/Downloads/L3S-GN1-20100130203947-00001/annotated/{}.html'
    
domains = {}
for h in urlmapping:
    if h:
        with open(template.format(h)) as f:
            html = f.read()
        tr = makeTree(html, h)
        if urlmapping[h][1] not in domains:
            domains[urlmapping[h][1]] = []
        domains[urlmapping[h][1]].append((urlmapping[h][0], h, tr))

filtered_domains = {}        
for x in domains:
    if len(domains[x]) > 1: 
        filtered_domains[x] = domains[x]

it = 0        
s = 0
fscores = []
for x in domains:
    for case in domains[x]:
        try:
            t = case[2]
            realy = normalize(''.join([x for x in t.xpath('//span[@class="x-nc-sel1"]/text()')]))
            ys = [x['text'] for x in getTitle(t,False)]
            #print(realy, '----------', y)
            it += 1 
            #if any([z in y for z in x.split('.')]):
            for y in ys:
                    if '-' in y or '|' in y:
                fscores.append(1)
                continue 
            f = f1(set(re.sub('[^a-zA-Z0-9]+', ' ', y.lower()).split()), set(re.sub('[^a-zA-Z0-9]+', ' ', realy.lower()).split()))
            fscores.append(f)
            y = " ".join(re.sub('[^a-zA-Z0-9]+', ' ', y.lower()).split())
            realy = " ".join(re.sub('[^a-zA-Z0-9]+', ' ', realy.lower()).split())
            if f < 1:
                print(realy, '-----------', y)
        except IndexError:
            pass
            
def f1(x,y):
    try:
        z = sum([w in y for w in x]) / len(x)
        z2 = sum([w in x for w in y]) / len(y)
        return (2 * z * z2) / (z + z2)
    except:
        return 0
    

it = 0        
s = 0
fscores = []
for x in domains:
    for case in domains[x]:
        try:
            t = case[2]
            realy = normalize(''.join([x for x in t.xpath('//span[@class="x-nc-sel1"]/text()')]))
            y = 1
            #print(realy, '----------', y)
            it += 1 
            #if any([z in y for z in x.split('.')]):
            f = f1(set(re.sub('[^a-zA-Z0-9]+', ' ', y.lower()).split()), set(re.sub('[^a-zA-Z0-9]+', ' ', realy.lower()).split()))
            fscores.append(f)
            y = " ".join(re.sub('[^a-zA-Z0-9]+', ' ', y.lower()).split())
            realy = " ".join(re.sub('[^a-zA-Z0-9]+', ' ', realy.lower()).split())
            if f < 1:
                print(realy, '-----------', y)
        except IndexError:
            pass

