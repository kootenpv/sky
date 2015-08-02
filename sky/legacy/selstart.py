from selenium.webdriver.common.keys import Keys
from selenium import webdriver    
from bs4 import BeautifulSoup
from threading import Thread
from threading import Lock 
import time
import random
import re

options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=/Users/pascal/Library/Application Support/Google/Chrome/Default')
driver = webdriver.Chrome(executable_path = '/Users/pascal/Downloads/chromedriver', chrome_options = options)
driver.set_window_size(1920, 1200)
driver.maximize_window()


def getCurrentSource():
    return BeautifulSoup(driver.page_source)

def getCurrentLinks():
    soup = getCurrentSource()
    return [x['href'] for x in soup.findAll('a', {'href' : True}) if x['href'].startswith('http://')]

while True:
    soup = getCurrentSource()
    links = [x['href'] for x in soup.findAll('a', {'href' : True}) if x['href'].startswith('http://')]
    random.shuffle(links)
    driver.get(links[0])
    time.sleep(2)
    
driver.find_element_by_tag_name("body").send_keys(Keys.COMMAND + "t")


div = '<div id="popup" style="display: none">some text here</div>'

'<div id="popup" style="display: inline">some text here</div>'

txt="""
var removePop = document.getElementById("elpopup");
if (removePop != null) { 
    removePop.parentElement.removeChild(removePop); 
}
elements = document.querySelectorAll(':hover');
var links = ''
var classesinfo = ''
for(var i = 0, element; (element = elements[i]) !== undefined; i++) {
  if (element.hasAttribute("href")) {
      links = links + " " + element.getAttribute('href')
  }
  if (element.hasAttribute("class")) {
      classesinfo = classesinfo + " " + element.getAttribute('class')
  }
}
if (elements != null && elements.length > 0) {
    var ele = elements[elements.length - 1];
    var para = document.createElement("div");
    var linksNode = document.createTextNode(links);
    var classesNode = document.createTextNode(classesinfo);
    para.setAttribute('id', 'elpopup')
    para.setAttribute('style', 'font-size:10px') 
    para.appendChild(linksNode);
    para.appendChild(classesNode);
    ele.appendChild(para);
}
"""

for i in range(20):
    links = getCurrentLinks()
    driver.execute_script(txt)
    time.sleep(0.5)
    print('tick ' + str(i))

path_to_chromedriver = '/Users/pascal/Downloads/chromedriver'
driver = webdriver.Chrome(executable_path = path_to_chromedriver)
driver.maximize_window()

driver.get('http://www.military-today.com/engineering/caterpillar_d9.htm')

var bla = []
document.addEventListener('click', function(e) {
    e = e || window.event;
    var mytarget = e.target || e.srcElement
    bla.push(getPathTo(mytarget))
}, false);

function getPathTo(element) {
    if (element.id!=='')
        return 'id("'+element.id+'")';
    if (element===document.body)
        return element.tagName;

    var ix= 0;
    var siblings= element.parentNode.childNodes;
    for (var i= 0; i<siblings.length; i++) {
        var sibling= siblings[i];
        if (sibling===element)
            return getPathTo(element.parentNode)+'/'+element.tagName+'['+(ix+1)+']';
        if (sibling.nodeType===1 && sibling.tagName===element.tagName)
            ix++;
    }
}

var keyboardMap = ["","","","CANCEL","","","HELP","","BACK_SPACE","TAB","","","CLEAR","ENTER","RETURN","","SHIFT","CONTROL","ALT","PAUSE","CAPS_LOCK","KANA","EISU","JUNJA","FINAL","HANJA","","ESCAPE","CONVERT","NONCONVERT","ACCEPT","MODECHANGE","SPACE","PAGE_UP","PAGE_DOWN","END","HOME","LEFT","UP","RIGHT","DOWN","SELECT","PRINT","EXECUTE","PRINTSCREEN","INSERT","DELETE","","0","1","2","3","4","5","6","7","8","9","COLON","SEMICOLON","LESS_THAN","EQUALS","GREATER_THAN","QUESTION_MARK","AT","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","WIN","","CONTEXT_MENU","","SLEEP","NUMPAD0","NUMPAD1","NUMPAD2","NUMPAD3","NUMPAD4","NUMPAD5","NUMPAD6","NUMPAD7","NUMPAD8","NUMPAD9","MULTIPLY","ADD","SEPARATOR","SUBTRACT","DECIMAL","DIVIDE","F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12","F13","F14","F15","F16","F17","F18","F19","F20","F21","F22","F23","F24","","","","","","","","","NUM_LOCK","SCROLL_LOCK","WIN_OEM_FJ_JISHO","WIN_OEM_FJ_MASSHOU","WIN_OEM_FJ_TOUROKU","WIN_OEM_FJ_LOYA","WIN_OEM_FJ_ROYA","","","","","","","","","","CIRCUMFLEX","EXCLAMATION","DOUBLE_QUOTE","HASH","DOLLAR","PERCENT","AMPERSAND","UNDERSCORE","OPEN_PAREN","CLOSE_PAREN","ASTERISK","PLUS","PIPE","HYPHEN_MINUS","OPEN_CURLY_BRACKET","CLOSE_CURLY_BRACKET","TILDE","","","","","VOLUME_MUTE","VOLUME_DOWN","VOLUME_UP","","","SEMICOLON","EQUALS","COMMA","MINUS","PERIOD","SLASH","BACK_QUOTE","","","","","","","","","","","","","","","","","","","","","","","","","","","OPEN_BRACKET","BACK_SLASH","CLOSE_BRACKET","QUOTE","","META","ALTGR","","WIN_ICO_HELP","WIN_ICO_00","","WIN_ICO_CLEAR","","","WIN_OEM_RESET","WIN_OEM_JUMP","WIN_OEM_PA1","WIN_OEM_PA2","WIN_OEM_PA3","WIN_OEM_WSCTRL","WIN_OEM_CUSEL","WIN_OEM_ATTN","WIN_OEM_FINISH","WIN_OEM_COPY","WIN_OEM_AUTO","WIN_OEM_ENLW","WIN_OEM_BACKTAB","ATTN","CRSEL","EXSEL","EREOF","PLAY","ZOOM","","PA1","WIN_OEM_CLEAR",""];

document.addEventListener("keydown", keyDownTextField, false);

function keyDownTextField(e) {
var keyCode = e.keyCode;
  bla.push(keyboardMap[keyCode])
}



ele = driver.find_element_by_xpath('id("comments-link-28888894")/A[1]')
ele.click()
ele = driver.switch_to_active_element()
ele.send_keys(67)


done_urls = set([''])

while True:
    try:
        current_url = slugify(driver.current_url) 
        if current_url in done_urls:
            continue
        done_urls.add(current_url)
        with open('/Users/pascal/GDrive/selenium_cache/' + current_url, 'w') as f: 
            f.write(driver.page_source)
        time.sleep(3)    
    except :
        print('err')
        opts = webdriver.ChromeOptions()
        opts.add_argument('--user-data-dir=/Users/pascal/Library/Application Support/Google/Chrome/Default')
        driver = webdriver.Chrome(executable_path = '/Users/pascal/Downloads/chromedriver', chrome_options = opts)
        driver.set_window_size(1920, 1200)
        driver.maximize_window() 
    
    

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import re
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    value = re.sub('[-\s]+', '-', value)
    return value



