# TITLE TESTS
try:
    from .training import Training
    from .helper import *
    from .findTitle import getTitle 
except SystemError:
    from training import Training    
    from helper import *
    from findTitle import getTitle 

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

