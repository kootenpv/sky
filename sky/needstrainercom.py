try:
    from .helper import getQuickTree
    from .findTitle import getTitle
except SystemError:
    from helper import getQuickTree
    from findTitle import getTitle

DOMAIN = 'http://theneeds.com'

ps = ["/news", "/shop", "/social", "/read", "/music", "/travel", "/video", "/sport", "/food", "/money", "/game", "/learn", "/work"]


seen = set()
titles = []
links = []
for p in ps:
    tree = getQuickTree(DOMAIN + p)
    for card in tree.xpath('//div[contains(@class, "view view-card")]'):
        sources = card.xpath('.//div[@class="view-card-source"]')
        titties = card.xpath('.//div[@class="view-card-title"]/a')
        descs = card.xpath('.//div[@class="view-card-descr"]')
        for s,t,d in zip(sources, titties, descs):
            stext = s.text_content().strip()
            if stext not in seen: 
                seen.add(stext)
                titles.append(t.text_content())
                links.append(t.get('data-href-ext'))
            
