import lxml.html
import justext

try:
    from .training import Training
    from .helper import *
except SystemError:
    from training import Training    
    from helper import *

def getTitle(tree, returnBest = True):
    # maybe lowercase wordsets, look at cases 37,38 and 53
    # we are now in overfitting terrain
    # consider regex on Title and title or just double
    # lets not ignore dash in class contains
    xpaths = ['//title', '//*[contains(@name, "title")]', '//h1[contains(@id, "title")]', '//h1[contains(@class, "title")]', '//h1[@*="title"]', '//*[contains(@id, "title")]',  '//meta[contains(@property, "title")]', '//meta[contains(@property, "title")]/@content', '//h1', '//h2', '//*[contains(@class, "title")]', '//*[@title]', '//h3', '//h4', '//strong', '//*[contains(@*, "headline")]', '//*[contains(@*, "Headline")]']
    # xpaths = ['//title', '//meta[contains(@property, "title")]', '//*[contains(@name, "title")]', '//h1[contains(@id, "title")]', '//h1[contains(@class, "title")]', '//h1[@*="title"]', '//*[contains(@id, "title")]', '//*[@*="title"]', '//*[contains(@class, "title")]', '//*[@title]', '//h1', '//h2', '//h3', '//h4']
    titles = []
    for xp in xpaths:
        xresults = tree.xpath(xp)
        title = {}
        for xresult in xresults:
            if isinstance(xresult, lxml.html.HtmlElement):
                title['text'] = xresult.text_content().strip()
            else:
                title['text'] = xresult   
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
