try:
    from .configs import DEFAULT_CRAWL_CONFIG
    from .scraper import Scrape
    from .helper import *
except:
    from configs import DEFAULT_CRAWL_CONFIG
    from scraper import Scrape 
    from helper import *

from sky.crawler import crawl

# Crawling 
CRAWL_CONFIG = DEFAULT_CRAWL_CONFIG
CRAWL_CONFIG.update({ 
    'seed_urls' : [ 
        'http://www.techcrunch.com/2015/05/21/chromebook-sales-predicted-to-grow-by-27-this-year-to-7-3m-units/'
    ],
    
    'collections_path' : '/Users/pascal/GDrive/sky_collections',

    'collection_name' : 'techie',

    # Optional
    
    'crawl_filter_strings' : [ 
        
    ],

    'crawl_required_strings' : [
        '2015', '2014'
    ],        
            
    'index_filter_strings' : [
        
    ],
    
    'index_required_strings' : [ 
        '2015', '2014'
    ], 

    'max_saved_responses' : 100,

    'max_workers' : 10,
})

crawl.start(CRAWL_CONFIG)

# Scrapeing

SCRAPE_CONFIG = CRAWL_CONFIG.copy()

SCRAPE_CONFIG.update({ 
    'template_proportion' : 0.09,
    'max_templates' : 1000
})

skindex = Scrape(SCRAPE_CONFIG)

res= skindex.process_all(remove_visuals = True)

url = 'http://www.huffingtonpost.com/2015/07/01/lord-rings-trivia_n_7688550.html?utm_hp_ref=weird-news&ir=Weird%20News'

view_tree(skindex.url_to_tree_mapping[url])



for x in res:
    print(res[x]['publish_date'])
