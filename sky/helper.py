# HTML(filename='/tmp/seleniumStringPage.html') 
import lxml.html
from selenium import webdriver

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import re
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    value = re.sub('[-\s]+', '-', value)
    return value

def viewString(x, driver):
    with open('/tmp/seleniumStringPage.html', 'w') as f:
        f.write(x)
    driver.get('file:///tmp/seleniumStringPage.html')

def makeParentLine(node, attach_head = False, questionContains = None):
    # Add how much text context is given. e.g. 2 would mean 2 parent's text nodes are also displayed
    if questionContains is not None:
        newstr = doesThisElementContain(questionContains, lxml.html.tostring(node))    
    else:
        newstr = lxml.html.tostring(node)        
    parent = node.getparent()
    while parent is not None:
        if attach_head and parent.tag == 'html': 
            newstr = lxml.html.tostring(parent.find('.//head'), encoding='utf8').decode('utf8') + newstr
        tag, items = parent.tag, parent.items()
        attrs = " ".join(['{}="{}"'.format(x[0], x[1]) for x in items if len(x) == 2])
        newstr = '<{} {}>{}</{}>'.format(tag, attrs, newstr, tag)
        parent = parent.getparent()
    return newstr    

def viewNode(node, attach_head = False, questionContains = None, save = False):
    try:
        driver = webdriver.Firefox()
        newstr = makeParentLine(node, attach_head, questionContains) 
        viewString(newstr, driver)    
        if save:
            driver.save_screenshot('pagination.png')    
        else:
            input('Waiting for input to continue... hit RETURN to quit.')    
    finally:
        driver.close()

def extractDomain(url): 
    tld = ".".join([x for x in tldextract.extract(url) if x ])
    protocol = url.split('//', 1)[0]
    if 'file:' == protocol:
        protocol += '///'
    else:
        protocol += '//'
    return protocol + tld    

def addBaseTag(node, url): 
    root = node.getroottree()
    if not root.find('.//base'):
        head = root.find('.//head')
        base = lxml.html.Element('base', attrib = {'href' : extractDomain(url)})
        head.insert(0, base)     

def doesThisElementContain(text = 'pagination', nodeStr = ''):
    templ = '<div style="border:2px solid lightgreen"><div style="background-color:lightgreen">Does this element contain <b>{}</b>?</div>{}</div>'
    return templ.format(text, nodeStr)


# url = 'https://www.kaggle.com/c/otto-group-product-classification-challenge/forums'
# driver = webdriver.Firefox()
# driver.get(url)
# html = driver.page_source
# driver.close()

# tree3 = lxml.html.fromstring(html)
# addBaseTag(tree3, url)
# lxml.html.tostring(head)

# viewNode(tree3, True, 'pagination', save=True)



