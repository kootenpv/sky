import sys
from selenium import webdriver
import lxml.html
import lxml.html.diff
import requests
from selenium.webdriver.common.keys import Keys

try:
    from .helper import viewString
except SystemError:
    from helper import viewString
        

def compareRequestsAndSelenium(url): 
    html1 = str(requests.get(url).text)
    try: 
        driver = webdriver.Firefox()
        driver.maximize_window() 
        driver.get(url) 
        html2 = str(driver.page_source) 
    finally:    
        driver.close()
    viewDiffHtml(url, html1, html2)    

def viewDiffHtml(url, html1, html2, diffMethod = lxml.html.diff.htmldiff):
    tree = lxml.html.fromstring(html1)
    tree2 = lxml.html.fromstring(html2)
    diffHtml = diffMethod(tree, tree2)
    diffTree = lxml.html.fromstring(diffHtml)
    insCounts = diffTree.xpath('count(//ins)')
    delCounts = diffTree.xpath('count(//del)')
    pureDiff = '' 
    for y in [z for z in diffTree.iter() if z.tag in ['ins', 'del']]:
        if y.text is not None:
            color = 'lightgreen' if 'ins' in y.tag else 'red'
            pureDiff += '<div style="background-color:{};">{}</div>'.format(color, y.text) 
    print('From non-javascript to javascript, {} insertions and {} deleted'.format(insCounts, delCounts)) 
    try:    
        driver = webdriver.Firefox()
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

# url = 'http://www.healthgrades.com/physician/dr-jeannine-villella-y4jts'
# compareRequestsAndSelenium(url)    

# url = 'https://www.betterdoctor.com/wendy-tcheng'
# compareRequestsAndSelenium(url)

if __name__ == '__main__':
    compareRequestsAndSelenium(sys.argv[1])
