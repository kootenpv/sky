import lxml.html

try:
    from .training import Training
    from .helper import *
except SystemError:
    from training import Training    
    from helper import *

def getBody(tree, returnBest = True):
    bodies = []
    for tag in ['div']:
        for att in ['id', 'class']:
            for val in ['article', 'content', 'main', 'body', 'page', 'container']: 
                xp = '//{}[contains(@{}, "{}")]'.format(tag, att, val)
                xres = tree.xpath(xp)
                body = {}
                if xres: 
                    if isinstance(xres[0], lxml.html.HtmlElement):
                        body['text'] = xres[0].text_content().strip()
                    else:
                        body['text'] = xres[0]   
                    if len(body['text']) < 3:
                        continue
                    #body['wordSet'] = set(x for x in body['text'].split() if len(x) > 1)
                    #body['wordSetLength'] = len(body['wordSet'])
                    body['xpath'] = xp
                    bodies.append(body) 
    if not returnBest:
        return bodies
    try:
        return bodies[0]['text']
    except:
        return ''

    t = bodies[0]
    for body in bodies[1:]:
        if len(t['wordSet'] & body['wordSet']) / len(t['wordSet']) > 0.3 and t['wordSetLength'] > body['wordSetLength']: 
            break
    else:
        body = t
    return body['text']


# tr = Training("nieuwsdumper-testcase1", "/Users/pascal/egoroot/virtual-python/sky/sky/tests/").load()
# tr2 = Training("marktplaats-testcase1", "/Users/pascal/egoroot/virtual-python/sky/sky/tests/").load()
# tr3 = Training("betterdoctor-doctor-referalls", "/Users/pascal/egoroot/virtual-python/sky/sky/tests/").load()

    
# train = [tr, tr2, tr3]            
# for t in train:
#     for tree in t.trees:
#         print(getTitle(tree))
            





            

