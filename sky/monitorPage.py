#!/usr/bin/env python3.4
import requests
import sys
import time
import lxml.html
from lxml.html.diff import htmldiff
from lxml.html.clean import Cleaner

url = sys.argv[1]

cleaner = Cleaner()
cleaner.javascript = True 
cleaner.style = True   
#cleaner.kill_tags = ['a', 'h1']
#cleaner.remove_tags = ['p']

def viewString(x, driver):
    with open('/tmp/seleniumStringPage.html', 'w') as f:
        f.write(x)
    driver.get('file:///tmp/seleniumStringPage.html')

def viewDiffHtml(tree1, tree2, diffMethod = htmldiff):
    diffHtml = diffMethod(tree1, tree2)
    diffTree = lxml.html.fromstring(diffHtml)
    insCounts = diffTree.xpath('count(//ins)')
    delCounts = diffTree.xpath('count(//del)')
    if insCounts + delCounts > 0:
        print('{} insertions and {} deleted'.format(insCounts, delCounts))
        for x in diffTree.xpath('//del'):
            print(lxml.html.tostring(x))
        for x in diffTree.xpath('//ins'):
            print(lxml.html.tostring(x)) 

old_html = requests.get(url).text
old_tree = lxml.html.fromstring(cleaner.clean_html(old_html))
old_content = old_tree.text_content()

while True:
    html = requests.get(url).text
    try:
        if html != old_html:
            tree = lxml.html.fromstring(cleaner.clean_html(html))
            content = tree.text_content()
            if content != old_content: 
                proportion_chars = sum([x == y for x,y in zip(html, old_html)]) / min(len(html), len(old_html))
                print('Proportion chars {}', proportion_chars) 
                viewDiffHtml(old_tree, tree)
                old_html = html 
                old_html = tree
                old_content = content 
    except requests.exceptions.ConnectionError: 
        print('ConnectionError')
        pass
    time.sleep(5)

    
