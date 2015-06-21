try:
    from .helper import getQuickTree
    from .findTitle import getTitle, getTitle2
    from .training import Training
except SystemError:
    from helper import getQuickTree
    from findTitle import getTitle, getTitle2
    from training import Training

DOMAIN = 'http://theneeds.com'

ps = ["/news", "/shop", "/social", "/read", "/music", "/travel", "/video", "/sport", "/food", "/money", "/game", "/learn", "/work"]


# seen = set()
# titles = []
# links = []
# for p in ps:
#     tree = getQuickTree(DOMAIN + p)
#     for card in tree.xpath('//div[contains(@class, "view view-card")]'):
#         sources = card.xpath('.//div[@class="view-card-source"]')
#         titties = card.xpath('.//div[@class="view-card-title"]/a')
#         descs = card.xpath('.//div[@class="view-card-descr"]')
#         for s,t,d in zip(sources, titties, descs):
#             stext = s.text_content().strip()
#             link = t.get('data-href-ext')
#             if stext not in seen: 
#                 if link is not None:
#                     seen.add(stext)
#                     titles.append(t.text_content())
#                     links.append(link)

# assert '\n' not in 'asdf'.join(titles)
# assert '\t' not in 'asdf'.join(titles)

# with open('theneeds.tsv', 'w') as f:
#     f.write('\n'.join(['{}\t{}'.format(l, t.replace('\n', ' ')) for l, t in zip(links,titles)]))

    

# tr = Training('titles', '/Users/pascal/GDrive/virtual-python/sky/sky/theneeds-test/').load()
# tr.addLinks(links[20:], False, len(tr.targets))
# tr.classify()
# tr.save()

