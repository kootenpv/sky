from sky.helper import fscore


def generate_rule_dictionary():
    headers = ['h{}'.format(i) for i in range(1, 5)]
    # tags = ['strong', 'b', 'div']
    tags = []
    atts = ['id', 'class', '']
    res = {k: {kk: {} for kk in atts} for k in headers + tags}
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
        # if maxi == 100:
            # maxi = dc[node.tag]['']['']
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


def getRuleTitle(tree, rule_dict=rule_dc):
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

# base_url = 'http://www.nieuwsdumper.nl/nieuws/'
# url2 = base_url + '1454/eerste-volvo-fmx-410-8x4-tridem-betonmixer-voor-bck.html'
# url3 = base_url + '1671/eerste-doosan-vijf-serie-in-friesland-afgeleverd-aan-kor-de-boer.html'

# tr = getQuickTree('http://www.bbc.com/news/world-africa-33049312')

# tr1 = getQuickTree('http://www.bbc.com/news/science-environment-33268180')

# tr2 = getQuickTree(url2)
# tr3 = getQuickTree(url3)

# rule_dict = generate_rule_dictionary()

# get_title_from_text_meta(tr, rule_dict)
