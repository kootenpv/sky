tree = lxml.html.fromstring(re.sub('\s+', ' ', str(html)))

tree2 = lxml.html.fromstring(re.sub('\s+', ' ', html2))

import selenium
from selenium import webdriver

import lxml.html



import lxml.html.diff as df



from urllib.request import urlopen

from selenium.webdriver.common.keys import Keys

tree2 = lxml.html.fromstring(html)



def viewString(x, driver):
    with open('/tmp/seleniumStringPage.html', 'w') as f:
        f.write(x)
    driver.get('file:///tmp/seleniumStringPage.html')

def testUrl(url): 
    try:
        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.get(url)
        html1 = str(urlopen(url).read()).replace('\\n','').replace('\\r','').replace("\\'", "'").replace("\\t", "\t")
        html2 = str(driver.page_source) 
        tree = lxml.html.fromstring(html1)
        tree2 = lxml.html.fromstring(html2)
        diffHtml = df.htmldiff(tree, tree2)
        diffTree = lxml.html.fromstring(diffHtml)
        insCounts = diffTree.xpath('count(//ins)')
        delCounts = diffTree.xpath('count(//del)')
        pureDiff = ''
        for x in ['.//ins', './/del']:
            for y in [z for z in diffTree.iter() if z.tag in ['ins', 'del']]:
                if y.text is not None:
                    color = 'lightgreen' if 'ins' in y.tag else 'red'
                    pureDiff += '<div style="background-color:{};">{}</div>'.format(color, y.text)
        print('From non-javascript to javascript, {} insertions and {} deleted'.format(insCounts, delCounts))
        diff = '<head><title>diff</title><base href=' + url + ' target="_blank"><style>ins{ background-color:lightgreen; } del{background-color:red;}</style></head>' +  diffHtml
        viewString(diff, driver) 
        driver.find_element_by_tag_name("body").send_keys(Keys.COMMAND + 't')
        viewString(html1, driver) 
        driver.find_element_by_tag_name("body").send_keys(Keys.COMMAND + 't')
        viewString(html2, driver) 
        driver.find_element_by_tag_name("body").send_keys(Keys.COMMAND + 't')
        viewString('<html><body>{}</body></html>'.format(str(pureDiff)), driver) 
    finally:    
        input('bla?')
        driver.close()

url = 'http://www.healthgrades.com/physician/dr-jeannine-villella-y4jts'
z=testUrl(url)    


attrs = ' '.join(y.keys())
