from sky.helper import fscore

############## Multi

def generate_rule_dictionary():
    headers = ['h{}'.format(i) for i in range(1, 5)]
    #tags = ['strong', 'b', 'div']
    tags = []
    atts = ['id', 'class', '']
    res = {k : {kk : {} for kk in atts} for k in headers + tags} 
    it = 0
    for h in headers:
        for k in atts:
            it += 1
            res[h][k]['title'] = it 
            it += 1
            res[h][k][''] = it
            it += 1    
        res[h]['']['title'] = it
        it += 1    
        res[h][''][''] = it
    # for t in tags:
    #     for k in atts:
    #         it += 1
    #         res[t][k]['title'] = it 
    #         it += 1
    #         res[t][k][''] = 100 
    #         it += 1
    #     res[t]['']['title'] = it    
    #     it += 1
    #     if t != 'div':
    #         res[t][''][''] = it    

    return res

def get_score_from_title_dict(node, dc):
    tag_found = dc.get(node.tag, '')
    if tag_found:
        maxi = 100
        for attribute in node.attrib:
            key_found = dc[node.tag].get(attribute, '')
            if key_found:
                if 'title' in node.attrib[attribute]: 
                    maxi = min(maxi, dc[node.tag][attribute]['title'])
                else:    
                    maxi = min(maxi, dc[node.tag][attribute][''])
        #if maxi == 100:
            #maxi = dc[node.tag][''][''] 
        return maxi, node.text_content()
    else:    
        return 101, ''
            
def get_meta_titles(tree): 
    res = []
    head = tree.find('head')
    if head is not None:
        for xp in ['.//title/text()', './/meta[contains(@name, "title")]/@content', 
                   './/meta[contains(@property, "title")]/@content']:
            res.extend(head.xpath(xp))
    return res                

def sorted_title_candidates(tree, rule_dict):
    mins = []            
    for node in tree.iter(): 
        score, ele = get_score_from_title_dict(node, rule_dict) 
        stripped_ele = ele.strip()
        if stripped_ele and score != 101:
            mins.append((score, stripped_ele))

    return [x[1] for x in sorted(mins)]

rule_dc = generate_rule_dictionary()
    
def getRuleTitle(tree, rule_dict = rule_dc):
    texts = sorted_title_candidates(tree, rule_dict)
    metas = get_meta_titles(tree)
    maxs = 0
    ele = ''
    for x in texts:
        xs = x.lower().split()
        for y in metas:            
            ys = y.lower().split()
            newm = fscore(xs, ys)
            if newm > maxs:
                maxs = newm
                ele = x
    return ele

# tr = getQuickTree('http://www.bbc.com/news/world-africa-33049312')

# tr1 = getQuickTree('http://www.bbc.com/news/science-environment-33268180')

# tr2 = getQuickTree('http://www.nieuwsdumper.nl/nieuws/1454/eerste-volvo-fmx-410-8x4-tridem-betonmixer-voor-bck.html')

# tr3 = getQuickTree('http://www.nieuwsdumper.nl/nieuws/1671/eerste-doosan-vijf-serie-in-friesland-afgeleverd-aan-kor-de-boer.html')

# rule_dict = generate_rule_dictionary()

# get_title_from_text_meta(tr, rule_dict)

###################################################################

###########  EXCLUDE FUCKING DICT HERE TEMPLATE STYLE


###################################################################

# def getTitle(tree, returnBest = True):
#     # maybe lowercase wordsets, look at cases 37,38 and 53
#     # we are now in overfitting terrain
#     # consider regex on Title and title or just double
#     # lets not ignore dash in class contains
#     xpaths = ['//title', '//*[contains(@name, "title")]', '//h1[contains(@id, "title")]', '//h1[contains(@class, "title")]', '//h1[@*="title"]', '//*[contains(@id, "title")]',  '//meta[contains(@property, "title")]', '//meta[contains(@property, "title")]/@content', '//h1', '//h2', '//*[contains(@class, "title")]', '//*[@title]', '//h3', '//h4', '//strong', '//*[contains(@*, "headline")]', '//*[contains(@*, "Headline")]']
#     # xpaths = ['//title', '//meta[contains(@property, "title")]', '//*[contains(@name, "title")]', '//h1[contains(@id, "title")]', '//h1[contains(@class, "title")]', '//h1[@*="title"]', '//*[contains(@id, "title")]', '//*[@*="title"]', '//*[contains(@class, "title")]', '//*[@title]', '//h1', '//h2', '//h3', '//h4']
#     titles = []
#     for xp in xpaths:
#         xresults = tree.xpath(xp)
#         title = {}
#         for xresult in xresults:
#             if isinstance(xresult, lxml.html.HtmlElement):
#                 title['text'] = xresult.text_content().strip()
#             else:
#                 title['text'] = xresult   
#             if len(title['text']) < 3:
#                 continue
#             title['wordSet'] = set(x for x in title['text'].split() if len(x) > 1)
#             title['wordSetLength'] = len(title['wordSet'])
#             title['xpath'] = xp
#             titles.append(title)

#     if not returnBest:
#         return titles

#     t = titles[0]
#     for title in titles[1:]:
#         if len(t['wordSet'] & title['wordSet']) / len(t['wordSet']) > 0.3 and t['wordSetLength'] > title['wordSetLength']: 
#             break
#     else:
#         title = t
#     return title['text']
