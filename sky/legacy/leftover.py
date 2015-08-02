from collections import Counter        

class SoupStats():
    def __init__(self, soup):
        self.soup = soup
        self.counter = Counter()
        for child in soup.findChildren():
            for atts in child.attrs.items():
                k,v = atts
                self.counter[atts] += 1
                self.counter[k] += 1
                self.counter[v] += 1

z = SoupStats(soup)        
        



counter = Counter()
for child in soup.findChildren():
    for atts in child.attrs.items():
        k,v = atts
        counter[k] += 1
        if isinstance(v, list):
            for l in v:
                counter[(k, l)] += 1
                counter[l] += 1
            counter[(k, " ".join(v))] += 1
        else:    
            counter[atts] += 1
            counter[v] += 1

