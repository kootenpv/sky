import sys
import requests

try:
    from .helper import *
except SystemError:
    from helper import *

def compareRequestsAndSelenium(url): 
    html1 = str(requests.get(url).text)
    try: 
        driver = webdriver.Firefox()
        driver.maximize_window() 
        driver.get(url) 
        html2 = str(driver.page_source) 
    finally:    
        driver.close()
    view_diff(url, html1, html2)    

    
# url = 'http://www.healthgrades.com/physician/dr-jeannine-villella-y4jts'
# compareRequestsAndSelenium(url)    

# url = 'https://www.betterdoctor.com/wendy-tcheng'
# compareRequestsAndSelenium(url)

if __name__ == '__main__':
    compareRequestsAndSelenium(sys.argv[1])
